#!/usr/bin/env python3
"""Proves the CI gates fail on real violations.

A gate that cannot fail gives false confidence, so each one is shown a bad input here.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_boundaries  # noqa: E402
import check_core_purity  # noqa: E402
import check_migrations  # noqa: E402


def graph(links: list[tuple[str, str]], extra: tuple[str, ...] = ()) -> str:
    """Builds a dot graph holding every target the rules name, plus the given links."""
    names = (
        set(check_boundaries.CORE_TARGETS)
        | {name for rule in check_boundaries.FORBIDDEN for name in rule[:2]}
        | {name for link in links for name in link}
        | set(extra)
    )
    ids = {name: f"node{index}" for index, name in enumerate(sorted(names))}
    lines = [f'"{ids[name]}" [ label = "{name}", shape = box ];' for name in names]
    lines += [f'"{ids[source]}" -> "{ids[target]}"' for source, target in links]
    return "\n".join(lines)


class BoundaryGate(unittest.TestCase):
    def test_clean_graph_passes(self) -> None:
        self.assertEqual(check_boundaries.check(graph([])), [])

    def test_direct_ledger_link_fails(self) -> None:
        errors = check_boundaries.check(graph([("fincero_ledger_inr", "fincero_ledger_cero")]))
        self.assertTrue(any("Rule 2" in error for error in errors))

    def test_indirect_link_fails(self) -> None:
        links = [("fincero_economy", "fincero_shim"), ("fincero_shim", "fincero_ledger_inr")]
        self.assertTrue(check_boundaries.check(graph(links)))

    def test_core_linking_third_party_fails(self) -> None:
        errors = check_boundaries.check(graph([("fincero_money", "Drogon::Drogon")]))
        self.assertTrue(any("core may depend only on core" in error for error in errors))

    def test_unlisted_target_reaching_rng_fails(self) -> None:
        errors = check_boundaries.check(graph([("fincero_assistant", "fincero_rng")]))
        self.assertTrue(any("Rule 7" in error for error in errors))

    def test_unlisted_target_reaching_rng_api_fails(self) -> None:
        errors = check_boundaries.check(graph([("fincero_assistant", "fincero_rng_api")]))
        self.assertTrue(any("Rule 7" in error for error in errors))

    def test_prediction_reaching_rng_fails(self) -> None:
        self.assertTrue(check_boundaries.check(graph([("fincero_prediction", "fincero_rng")])))

    def test_market_may_reach_rng(self) -> None:
        self.assertEqual(check_boundaries.check(graph([("fincero_market", "fincero_rng")])), [])

    def test_stale_rule_fails(self) -> None:
        errors = check_boundaries.check('"node0" [ label = "fincero_base" ];')
        self.assertTrue(any("stale rule" in error for error in errors))


class PurityGate(unittest.TestCase):
    def violations(self, relative: str, source: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text(source, encoding="utf-8")
            return check_core_purity.check_tree(root)

    def test_clean_source_passes(self) -> None:
        self.assertEqual(self.violations("money/src/a.cpp", "int add(int a, int b);\n"), [])

    def test_banned_header_fails(self) -> None:
        self.assertTrue(self.violations("rng/src/a.cpp", "#include <chrono>\n"))

    def test_global_rng_fails(self) -> None:
        self.assertTrue(self.violations("rng/src/a.cpp", "int f() { return rand(); }\n"))

    def test_random_device_fails(self) -> None:
        self.assertTrue(self.violations("rng/src/a.cpp", "std::random_device device;\n"))

    def test_clock_fails(self) -> None:
        self.assertTrue(self.violations("market/src/a.cpp", "auto t = time(nullptr);\n"))

    def test_float_in_money_fails(self) -> None:
        self.assertTrue(self.violations("money/src/a.cpp", "double balance = 0;\n"))

    def test_float_allowed_in_prediction(self) -> None:
        self.assertEqual(self.violations("prediction/src/a.cpp", "double band = 0;\n"), [])

    def test_words_in_comments_pass(self) -> None:
        source = '// never call rand() or use double\nconst char* s = "rand()";\n'
        self.assertEqual(self.violations("money/src/a.cpp", source), [])

    def test_tests_folder_is_skipped(self) -> None:
        self.assertEqual(self.violations("rng/tests/a.cpp", "#include <fstream>\n"), [])


class MigrationGate(unittest.TestCase):
    def test_clean_migration_passes(self) -> None:
        text = "-- migrate:up\nCREATE TABLE cero.accounts (id BIGINT);\n-- migrate:down\n"
        self.assertEqual(check_migrations.check_text("a.sql", text), [])

    def test_down_body_fails(self) -> None:
        text = "-- migrate:up\nSELECT 1;\n-- migrate:down\nDROP TABLE x;\n"
        self.assertTrue(check_migrations.check_text("a.sql", text))

    def test_missing_down_fails(self) -> None:
        self.assertTrue(check_migrations.check_text("a.sql", "-- migrate:up\nSELECT 1;\n"))

    def test_cross_ledger_migration_fails(self) -> None:
        text = (
            "-- migrate:up\n"
            "ALTER TABLE cero.grants ADD FOREIGN KEY (p) REFERENCES inr.payments (id);\n"
            "-- migrate:down\n"
        )
        errors = check_migrations.check_text("a.sql", text)
        self.assertTrue(any("Rule 2" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
