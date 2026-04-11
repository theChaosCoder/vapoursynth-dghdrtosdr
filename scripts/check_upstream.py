#!/usr/bin/env python3
"""Checks for new DGHDRtoSDR releases"""
import os, re, sys, urllib.request

INDEX_URL = "https://rationalqm.us/hdr/"
HEADERS = {"User-Agent": "VSRepo"}
PATTERN = re.compile(r"DGHDRtoSDR_(\d+\.\d+)\.rar")

req = urllib.request.Request(INDEX_URL, headers=HEADERS)
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode("utf-8", errors="ignore")

versions = sorted(set(PATTERN.findall(html)), key=lambda v: tuple(map(int, v.split("."))))
if not versions:
    print("::error::No Version found")
    sys.exit(2)

latest = versions[-1]
print(f"Upstream latest: {latest}")

# Last known Version on PyPI
try:
    with urllib.request.urlopen("https://pypi.org/pypi/vapoursynth-dghdrtosdr/json", timeout=15) as r:
        import json
        published = json.load(r)["info"]["version"]
except Exception:
    published = "0.0.0"
print(f"PyPI latest:     {published}")


gh_out = os.environ.get("GITHUB_OUTPUT")
if gh_out:
    with open(gh_out, "a") as f:
        f.write(f"upstream={latest}\n")
        f.write(f"published={published}\n")
        f.write(f"is_new={'true' if latest != published else 'false'}\n")

sys.exit(0 if latest == published else 1)
