#!/usr/bin/env python3

from __future__ import annotations

import importlib.machinery
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


HELPER = Path(__file__).parents[1] / "bin" / "photography-ticket-delivery"


def load_helper():
    loader = importlib.machinery.SourceFileLoader("photography_ticket_delivery", str(HELPER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("cannot load photography-ticket-delivery")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


delivery = load_helper()


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


class AmendmentHistoryTests(unittest.TestCase):
    def test_legacy_state_without_amendments_remains_valid(self) -> None:
        state = {"publication_commit": "a" * 40}
        self.assertEqual(delivery.validate_amendment_chain(state), [])

    def test_valid_append_only_chain_ends_at_current_publication(self) -> None:
        first = "a" * 40
        second = "b" * 40
        third = "c" * 40
        state = {
            "initial_publication_commit": first,
            "publication_commit": third,
            "amendments": [
                {
                    "previous_publication_commit": first,
                    "publication_commit": second,
                },
                {
                    "previous_publication_commit": second,
                    "publication_commit": third,
                },
            ],
        }
        self.assertEqual(len(delivery.validate_amendment_chain(state)), 2)

    def test_broken_chain_is_rejected(self) -> None:
        state = {
            "initial_publication_commit": "a" * 40,
            "publication_commit": "c" * 40,
            "amendments": [
                {
                    "previous_publication_commit": "b" * 40,
                    "publication_commit": "c" * 40,
                }
            ],
        }
        with self.assertRaisesRegex(delivery.DeliveryError, "append-only commit chain"):
            delivery.validate_amendment_chain(state)

    def test_comment_renders_original_and_amended_immutable_evidence(self) -> None:
        first = "a" * 40
        second = "b" * 40
        state = {
            "issue": 17,
            "ticket": "MEDIA-03",
            "evidence": "docs/acceptance/MEDIA-03-ACCEPTANCE-EVIDENCE.md",
            "published_at": "2026-08-13T10:54:08+00:00",
            "initial_publication_commit": first,
            "publication_commit": second,
            "amendments": [
                {
                    "previous_publication_commit": first,
                    "publication_commit": second,
                    "amended_at": "2026-08-13T15:00:00+00:00",
                }
            ],
        }
        body = delivery.evidence_comment_body(
            state, second, {"url": "https://github.com/example/pull/62"}
        )
        self.assertIn(delivery.immutable_commit_url(first), body)
        self.assertIn(delivery.immutable_commit_url(second), body)
        self.assertIn(delivery.immutable_evidence_url(first, state["evidence"]), body)
        self.assertIn(delivery.immutable_evidence_url(second, state["evidence"]), body)
        self.assertIn("### Publication history", body)


class AmendmentDeltaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Delivery Test")
        git(self.root, "config", "user.email", "delivery-test@example.invalid")
        (self.root / "allowed.txt").write_text("one\n")
        (self.root / "outside.txt").write_text("one\n")
        (self.root / "evidence.md").write_text("evidence\n")
        git(self.root, "add", "allowed.txt", "outside.txt", "evidence.md")
        git(self.root, "commit", "-q", "-m", "base")
        self.base = git(self.root, "rev-parse", "HEAD")
        self.previous_app_repo = delivery.APP_REPO
        delivery.APP_REPO = self.root

    def tearDown(self) -> None:
        delivery.APP_REPO = self.previous_app_repo
        self.temporary.cleanup()

    def commit_change(self, path: str, content: str, message: str) -> str:
        (self.root / path).write_text(content)
        git(self.root, "add", path)
        git(self.root, "commit", "-q", "-m", message)
        return git(self.root, "rev-parse", "HEAD")

    def test_modified_attested_path_is_allowed_and_evidence_oid_is_stable(self) -> None:
        amended = self.commit_change("allowed.txt", "two\n", "modify allowed")
        self.assertEqual(
            delivery.amendment_delta(self.base, amended, ["allowed.txt", "evidence.md"]),
            [{"path": "allowed.txt", "status": "M"}],
        )
        self.assertEqual(
            delivery.commit_blob_oid(self.base, "evidence.md"),
            delivery.commit_blob_oid(amended, "evidence.md"),
        )

    def test_same_commit_is_not_a_strict_descendant(self) -> None:
        with self.assertRaisesRegex(delivery.DeliveryError, "strictly descend"):
            delivery.amendment_delta(self.base, self.base, ["allowed.txt"])

    def test_new_path_is_rejected(self) -> None:
        amended = self.commit_change("new.txt", "new\n", "add path")
        with self.assertRaisesRegex(delivery.DeliveryError, "may only modify"):
            delivery.amendment_delta(self.base, amended, ["allowed.txt"])

    def test_deleted_path_is_rejected(self) -> None:
        (self.root / "allowed.txt").unlink()
        git(self.root, "add", "allowed.txt")
        git(self.root, "commit", "-q", "-m", "delete path")
        amended = git(self.root, "rev-parse", "HEAD")
        with self.assertRaisesRegex(delivery.DeliveryError, "may only modify"):
            delivery.amendment_delta(self.base, amended, ["allowed.txt"])

    def test_non_descendant_commit_is_rejected(self) -> None:
        first = self.commit_change("allowed.txt", "two\n", "first child")
        git(self.root, "switch", "-q", "-c", "sibling", self.base)
        sibling = self.commit_change("allowed.txt", "three\n", "sibling child")
        with self.assertRaisesRegex(delivery.DeliveryError, "does not descend"):
            delivery.amendment_delta(first, sibling, ["allowed.txt"])

    def test_modified_path_outside_original_manifest_is_rejected(self) -> None:
        amended = self.commit_change("outside.txt", "two\n", "modify outside")
        with self.assertRaisesRegex(delivery.DeliveryError, "outside the original"):
            delivery.amendment_delta(self.base, amended, ["allowed.txt"])

    def test_changed_evidence_blob_is_detectable(self) -> None:
        amended = self.commit_change("evidence.md", "different\n", "change evidence")
        self.assertNotEqual(
            delivery.commit_blob_oid(self.base, "evidence.md"),
            delivery.commit_blob_oid(amended, "evidence.md"),
        )


class ParserTests(unittest.TestCase):
    def test_amend_command_requires_exact_identity_and_verdict_inputs(self) -> None:
        args = delivery.build_parser().parse_args(
            [
                "amend",
                "--issue",
                "17",
                "--ticket",
                "MEDIA-03",
                "--base",
                "backend",
                "--commit",
                "c" * 40,
                "--verdict",
                "PASS",
            ]
        )
        self.assertIs(args.handler, delivery.command_amend)


if __name__ == "__main__":
    unittest.main()
