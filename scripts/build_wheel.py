#!/usr/bin/env python3
"""Build Wheel"""
import os, re, shutil, subprocess, sys, urllib.request
from pathlib import Path

VERSION = os.environ["UPSTREAM_VERSION"]  # "1.16"
URL = f"https://rationalqm.us/hdr/DGHDRtoSDR_{VERSION}.rar"
ROOT = Path(__file__).resolve().parent.parent
PAYLOAD = ROOT / "build_payload"
TMP = ROOT / "_tmp"

# clean up
for p in (PAYLOAD, TMP):
    if p.exists(): shutil.rmtree(p)
PAYLOAD.mkdir(); TMP.mkdir()

# Download with VSRepo User-Agent
print(f"Lade {URL}")
req = urllib.request.Request(URL, headers={"User-Agent": "VSRepo"})
rar_path = TMP / "plugin.rar"
with urllib.request.urlopen(req, timeout=60) as r, open(rar_path, "wb") as f:
    shutil.copyfileobj(r, f)

subprocess.run(["unar", "-o", str(TMP), str(rar_path)], check=True)

extracted_root = next(p for p in TMP.iterdir() if p.is_dir() and p.name != "plugin.rar")
print(f"Archive root: {extracted_root}")
for item in extracted_root.iterdir():
    if item.is_dir():
        print(f"  Skip dir: {item.name}")
        continue
    print(f"  Include: {item.name}")
    shutil.copy2(item, PAYLOAD / item.name)

# Sanity check
dlls = list(PAYLOAD.glob("*.dll"))
if not dlls:
    sys.exit("Error: no .dll found in /")

# Version in pyproject.toml setzen
pyproject = ROOT / "pyproject.toml"
text = pyproject.read_text()
text = re.sub(r'^version = "[^"]*"', f'version = "{VERSION}"', text, count=1, flags=re.M)
pyproject.write_text(text)

# Build wheel + tag as win_amd64
subprocess.run([sys.executable, "-m", "build", "--wheel"], check=True)
wheel = next((ROOT / "dist").glob("*.whl"))
subprocess.run(["wheel", "tags", "--platform-tag", "win_amd64", "--remove", str(wheel)], check=True)
print("Done:", list((ROOT / "dist").glob("*.whl")))
