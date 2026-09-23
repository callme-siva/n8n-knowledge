"""Regenerate every workflow + README:  python3 tools/build.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import level1_2, level3_4

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for fn in level1_2.ALL + level3_4.ALL:
    fn(ROOT)
    print("built", fn.__name__)
