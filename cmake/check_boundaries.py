#!/usr/bin/env python3
"""Fail if the real CMake target graph crosses a module boundary.

Input is the dot file from `cmake --graphviz`. Rules apply to everything a target can
reach, directly or indirectly, so a forbidden link cannot hide behind another target.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

NODE = re.compile(r'"(node\d+)"\s*\[\s*label\s*=\s*"([^"]+)"')
EDGE = re.compile(r'"(node\d+)"\s*->\s*"(node\d+)"')

# Everything allowed inside core. Core may link nothing else (CLAUDE.md, Conventions).
CORE_TARGETS = {
    "fincero_base",
    "fincero_money",
    "fincero_upi_text",
    "fincero_ledger_rules",
    "fincero_txn",
    "fincero_rng",
    "fincero_market_model",
    "fincero_economy_rules",
    "fincero_prediction",
}

# (from, must not reach, why)
FORBIDDEN = [
    ("fincero_ledger_inr", "fincero_ledger_cero", "Rule 2: the two ledgers share no path"),
    ("fincero_ledger_cero", "fincero_ledger_inr", "Rule 2: the two ledgers share no path"),
    ("fincero_economy", "fincero_ledger_inr", "Rule 2: earning uses events, not the INR ledger"),
    ("fincero_market", "fincero_ledger_inr", "Rule 2: the market runs on ceros only"),
    ("fincero_prediction", "fincero_rng", "Rule 7: predictions use history only"),
    ("fincero_market_model", "fincero_rng", "Digits are an input to the price model"),
    ("fincero_core_client", "fincero_rng", "Rule 7: RNG never ships to clients"),
    ("fincero_client_binding", "fincero_rng", "Rule 7: RNG never ships to clients"),
    ("fincero_client_binding", "fincero_market_model", "Clients get money formatting only"),
]

# The only targets that may reach the RNG. Test binaries are matched by suffix.
RNG_ALLOWED = {
    "fincero_rng",
    "fincero_core",
    "fincero_market",
    "fincero_server",
    "fincero_econ_sim",
    "fincero_market_replay",
}


def parse(text: str) -> tuple[dict[str, str], dict[str, set[str]]]:
    """Returns node id -> label, and adjacency by label."""
    labels = dict(NODE.findall(text))
    edges: dict[str, set[str]] = defaultdict(set)
    for source, target in EDGE.findall(text):
        if source in labels and target in labels:
            edges[labels[source]].add(labels[target])
    return labels, edges


def reachable(start: str, edges: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    stack = list(edges.get(start, ()))
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(edges.get(node, ()))
    return seen


def check(text: str) -> list[str]:
    labels, edges = parse(text)
    known = set(labels.values())
    errors: list[str] = []

    # A rule naming a target that no longer exists would pass forever, so that fails too.
    named = CORE_TARGETS | {name for rule in FORBIDDEN for name in rule[:2]}
    for name in sorted(named - known):
        errors.append(f"stale rule: target {name} is not in the graph")

    for target in sorted(CORE_TARGETS & known):
        for dep in sorted(reachable(target, edges) - CORE_TARGETS):
            errors.append(f"{target} links {dep}: core may depend only on core")

    for source, banned, why in FORBIDDEN:
        if source in known and banned in reachable(source, edges):
            errors.append(f"{source} reaches {banned}: {why}")

    for target in sorted(known):
        if target in RNG_ALLOWED or target.endswith("_tests"):
            continue
        if "fincero_rng" in reachable(target, edges):
            errors.append(f"{target} reaches fincero_rng: only the market may (Rule 7)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dot_file", type=Path)
    args = parser.parse_args()

    errors = check(args.dot_file.read_text(encoding="utf-8"))
    for error in errors:
        print(f"boundary violation: {error}", file=sys.stderr)
    if not errors:
        print("module boundaries ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
