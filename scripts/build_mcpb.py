#!/usr/bin/env python
"""Build an MCPB (.mcpb) bundle for foodcalorie-mcp.

MCPB = MCP Bundle: a zip archive with manifest.json + server code that
Claude Desktop (and Smithery / other MCPB-aware clients) can install with
one click. Spec: https://github.com/modelcontextprotocol/mcpb

The bundle does not vendor dependencies. It declares a `uv` runtime that
installs the published PyPI release on first run, so the bundle stays tiny
and always tracks the released artifact rather than a copy of it.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PKG = "foodcalorie-mcp"


def read_version() -> str:
    for line in (ROOT / "pyproject.toml").read_text(encoding="utf-8").splitlines():
        if line.startswith("version ="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("version not found in pyproject.toml")


def tools_from_snapshot() -> list[dict]:
    snap = ROOT / "tools_snapshot.json"
    if not snap.exists():
        return []
    data = json.loads(snap.read_text(encoding="utf-8"))
    out = []
    for t in data:
        desc = (t.get("description") or "").strip().split("\n")[0]
        out.append({"name": t["name"], "description": desc})
    return out


def build_manifest(version: str) -> dict:
    return {
        "manifest_version": "0.3",
        "name": "foodcalorie-mcp",
        "display_name": "FoodCalorie China",
        "version": version,
        "description": (
            "Chinese chain-restaurant calories and macros for 103 real menu items "
            "across 14 chains. Read-only, no API key."
        ),
        "long_description": (
            "Real nutrition data for Chinese chain-restaurant menus -- the food people "
            "actually eat, not a generic USDA lookup.\n\n"
            "Coverage: 103 menu items across 14 chains (Starbucks China, Luckin, Heytea, "
            "Nayuki, Chagee, Mixue, KFC China, McDonald's China and others). Every item "
            "carries calories, protein, fat, carbohydrate, plus a per-item health note.\n\n"
            "Six tools: look up by barcode, search by name (Chinese or English), list by "
            "category, compare several items side by side, sum a day's intake, and pull a "
            "health tip for a given item.\n\n"
            "Read-only. No account, no API key, no network calls beyond the packaged data. "
            "Pro datasets with wider coverage are available separately; this bundle is the "
            "free tier and says so everywhere it could be ambiguous."
        ),
        "author": {
            "name": "Haochang Ji",
            "email": "jihaochang1@users.noreply.github.com",
            "url": "https://jihaochang1.github.io/foodcalorie-pro/en.html",
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/Jihaochang1/foodcalorie-mcp",
        },
        "homepage": "https://jihaochang1.github.io/foodcalorie-pro/en.html",
        "documentation": "https://github.com/Jihaochang1/foodcalorie-mcp#readme",
        "support": "https://github.com/Jihaochang1/foodcalorie-mcp/issues",
        "license": "Apache-2.0",
        "keywords": [
            "nutrition",
            "calorie",
            "chinese-food",
            "diet",
            "health",
            "macro",
            "mcp",
        ],
        "server": {
            "type": "python",
            "entry_point": "server/main.py",
            "mcp_config": {
                "command": "uv",
                "args": [
                    "run",
                    "--python",
                    "3.12",
                    "--with",
                    f"{PKG}=={version}",
                    PKG,
                ],
            },
        },
        "tools": tools_from_snapshot(),
        "compatibility": {
            "claude_desktop": ">=0.10.0",
            "platforms": ["darwin", "win32", "linux"],
            "runtimes": {"python": ">=3.12"},
        },
    }


LAUNCHER = '''"""Entry point for the MCPB bundle.

The real implementation ships on PyPI. `manifest.json` runs this module via
`uv run --with foodcalorie-mcp==<version>`, which puts the package on
sys.path before this file executes. Running it standalone (without uv) fails
with an import error, which is the intended signal that the bundle was
launched outside its declared runtime.
"""

from foodcalorie_mcp.server import main

if __name__ == "__main__":
    main()
'''


def main() -> None:
    version = read_version()
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{PKG}-{version}.mcpb"

    manifest = build_manifest(version)
    if not manifest["tools"]:
        raise SystemExit("tools_snapshot.json missing or empty -- run the introspection export first")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        z.writestr("server/main.py", LAUNCHER)
        z.writestr(
            "README.md",
            "# FoodCalorie China (MCPB bundle)\n\n"
            "Install into Claude Desktop, or point any MCPB-aware client at this file.\n\n"
            f"Version {version}. Data: 103 items / 14 chains. Free tier.\n",
        )

    size = out.stat().st_size
    names = zipfile.ZipFile(out).namelist()
    print(f"built {out} ({size} bytes, {len(names)} entries)")
    for n in names:
        print("  ", n)
    print(f"tools declared: {len(manifest['tools'])}")


if __name__ == "__main__":
    main()
