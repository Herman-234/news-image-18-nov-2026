#!/usr/bin/env python3
"""news-image-20261118 entry: copy the rendered summary image to /output/entry.png.

Runs on Python 3.13 with the standard library only and no network. The image
(entry.png) was drawn locally by render.py from the verified news of Wednesday
18 November 2026; this program only copies its exact bytes, so both grader
runs write identical output.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(
    os.path.join(HERE, "entry.png"),
    os.path.join(OUT, "entry.png"),
)
