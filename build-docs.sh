#!/usr/bin/env bash
# Docs build: pre-render the shipped SKILL.md files into static HTML pages.
# Docs can't drift from code — this runs on every deploy (see vercel.json).
set -euo pipefail
cd "$(dirname "$0")"
python3 -c "import markdown" 2>/dev/null || pip install markdown -q || true
python3 scripts/md_render.py
# showcase assets are committed in docs-site/showcase/ — nothing to copy or fetch.
echo "docs-site ready: $(ls docs-site/docs | wc -l | tr -d ' ') doc pages + landing"
