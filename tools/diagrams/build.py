#!/usr/bin/env python3
"""Build every diagram into docs/images/.

    python3 tools/diagrams/build.py            # all
    python3 tools/diagrams/build.py banner     # one
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import diagrams  # noqa: E402
import importlib  # noqa: E402

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "docs", "images"))

# file name -> function
BUILD = {
    "banner": diagrams.banner,
    "architecture": diagrams.architecture,
    "route": diagrams.route,
}
for modname in ("diagrams_b", "diagrams_c", "diagrams_d"):
    try:
        mod = importlib.import_module(modname)
    except ModuleNotFoundError:
        continue
    BUILD.update({k: getattr(mod, k) for k in mod.ALL})


def main():
    want = sys.argv[1:] or list(BUILD)
    os.makedirs(OUT, exist_ok=True)
    for name in want:
        canvas = BUILD[name]()
        path = os.path.join(OUT, f"{name}.svg")
        canvas.save(path)
        print(f"wrote {path}  ({canvas.w}x{canvas.h})")


if __name__ == "__main__":
    main()
