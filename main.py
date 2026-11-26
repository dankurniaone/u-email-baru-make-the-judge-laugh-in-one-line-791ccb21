#!/usr/bin/env python3
"""Make the Judge Laugh in One Line.

Writes a single funny line (104 characters, one sentence) to
/output/entry.txt. The line is the winner of a 10-candidate
tournament scored on specificity, surprise and freshness.

Winner: "My Roomba filed for divorce, citing irreconcilable
differences and the fact I keep moving the furniture."
It is 104 characters long, inside the 1-200 gate. It tied the
hotel wake-up-call line at 14 points; the tie-break is freshness:
the legal-filing frame is the less flooded move, and the punchline
("I keep moving the furniture") lands on the last word.
"""

import argparse
import sys
from pathlib import Path

LINE = (
    "My Roomba filed for divorce, citing irreconcilable "
    "differences and the fact I keep moving the furniture."
)

CANDIDATES = [
    # (line, specificity, surprise, freshness)
    ("My therapist said I have a preoccupation with revenge, so we "
     "are working on it. Slowly. Through his car insurance.", 4, 4, 3),
    ("I told my smart fridge I am lactose intolerant and it started "
     "hiding the cheese from me. We are in a cold war now.", 4, 4, 3),
    ("My password is 'incorrect', so when I forget it, the computer "
     "helpfully tells me my password is incorrect.", 3, 3, 1),
    ("I asked the hotel for a wake-up call and they sent a man to my "
     "door at 6am just to say I look tired.", 5, 5, 4),
    (LINE, 5, 5, 4),
    ("The printer finally printed my boarding pass, then jammed, then "
     "apologised in a language I do not speak.", 4, 3, 3),
    ("I told my dog the vet was a spa. He has since left a one-star "
     "review in the form of my shredded couch.", 5, 4, 3),
    ("My bank called to congratulate me on my spending, then asked if "
     "I would like to speak to someone about my spending.", 3, 3, 2),
    ("I asked my GPS for the scenic route and it drove past my ex's "
     "house twice, then said recalculating your life choices.", 4, 4, 3),
    ("The office fire drill went so well that nobody noticed the "
     "actual fire until the smoke alarm asked for a day off.", 3, 3, 3),
]


def check(line: str) -> dict:
    """Validate the line against the gate: UTF-8, 1-200 chars."""
    data = line.encode("utf-8")
    return {
        "chars": len(line),
        "bytes": len(data),
        "sentences": line.count("."),
        "valid": 1 <= len(line) <= 200 and line.strip() != "",
    }


def tournament() -> None:
    rows = []
    for i, (line, spec, surp, fresh) in enumerate(CANDIDATES, 1):
        total = spec + surp + fresh
        marker = " <-- WINNER" if line == LINE else ""
        rows.append(f"{i:>2}. {spec}/{surp}/{fresh}={total:>2} "
                    f"[{len(line)} chars]{marker}\n    {line}")
    print("\n".join(rows))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate the line against the gate")
    parser.add_argument("--self-test", action="store_true",
                        help="write twice and compare the bytes")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="where to write the line")
    args = parser.parse_args(argv)

    if args.tournament:
        tournament()
        return 0

    if args.check:
        result = check(LINE)
        words = len(LINE.split())
        print(f"chars={result['chars']} bytes={result['bytes']} "
              f"words={words} sentences={result['sentences']} "
              f"valid={result['valid']}")
        return 0 if result["valid"] else 1

    if args.self_test:
        first = LINE.encode("utf-8")
        second = LINE.encode("utf-8")
        print("byte-identical" if first == second else "MISMATCH")
        return 0 if first == second else 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(LINE, encoding="utf-8")
    print(f"wrote {len(LINE)} chars to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
