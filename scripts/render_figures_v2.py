#!/usr/bin/env python3
"""Render the revised (V2) main and supplementary figures from stored inputs."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from flyvis_midd.figure_rendering_v2 import ALL, render

if __name__ == "__main__":
    for key in sys.argv[1:] or ALL:
        render(key)
