#!/usr/bin/env python3
"""Copy the committed front-page image into the output directory.

The entry image is produced by draw.py and committed as entry.png.
This program just places a copy where the grader expects it:
the directory named by MAKEFUN_OUTPUT_DIR (or "output" when unset).
Standard library only.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    if not os.path.isfile(SRC):
        print("entry.png not found next to main.py; run draw.py first",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.getcwd(), out_dir)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    print("copied entry.png (%d bytes) to %s"
          % (os.path.getsize(dest), dest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
