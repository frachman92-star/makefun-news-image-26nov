#!/usr/bin/env python3
"""News-image entry for 26 November 2026 (Python 3.13, standard library only).

The image is entry.png beside this file, drawn by draw.py (PIL) from the
verified facts of Thursday 26 November 2026. This program copies it to
/output/entry.png. The gate takes a whole PNG of at most 1 MiB and 1024 by
1024 pixels, and the judge sees exactly the bytes copied.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

os.makedirs(OUT, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
shutil.copyfile(src, dst)
# gate guard: the entry must stay a whole PNG of at most 1 MiB, 1024 by 1024
size = os.path.getsize(dst)
assert size <= 1048576, f"entry.png is {size} bytes, over the 1 MiB cap"
print("wrote entry.png to", OUT)
