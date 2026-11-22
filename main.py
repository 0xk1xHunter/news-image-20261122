#!/usr/bin/env python3
"""Entry point for news-image-20261122.

The front page for Sunday 22 November 2026 was drawn in advance by
draw.py (PIL) and committed as entry.png next to this file. The grader
runs this program with no network and stdlib only, so all it does is copy
that committed image to the output directory, byte for byte, every time.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("missing committed entry.png next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
