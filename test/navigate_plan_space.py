#!/usr/bin/env python3
"""Navigate the plan space of blocks.lp with fasb.

Run inside the project environment (which provides the fasb bindings):

    uv run test/navigate_plan_space.py [--horizon 12] [program.lp]

Reports, for the empty route (the whole plan space):
  * the facet count            (fasb `count` / `#?`)
  * the plan count             (fasb `solvecount` / `#!`)
  * the significance of every facet (fasb `counts` / `#??`)
"""

import argparse
from pathlib import Path

from fasb import interpreter_bindings as ib
from fasb import wrappers_bindings as wb

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "program",
        nargs="?",
        default=str(HERE / "blocks.lp"),
        help="logic program encoding the planning problem (default: blocks.lp)",
    )
    parser.add_argument(
        "--horizon", type=int, default=12, help="plan length bound (default: 12)"
    )
    args = parser.parse_args()

    program = Path(args.program).read_text()
    # "0" = enumerate all models; -c horizon=N overrides the #const in the program.
    nav = wb.PyNavigator(program, ["0", "-c", f"horizon={args.horizon}"])

    route = []  # empty route: the whole plan space
    facets = ib.compute_facets(nav, route, [])

    # The bindings print to stdout from Rust, so flush the headers to keep the
    # interleaving right.
    print(f"\nfacet count (horizon={args.horizon}):", flush=True)
    ib.facet_count(facets)

    print("\nplan count:", flush=True)
    ib.answer_set_count(nav, route, [])

    print("\nfacet significance (significance, remaining facets, facet):", flush=True)
    ib.facet_counts(nav, facets, route, [])


if __name__ == "__main__":
    main()
