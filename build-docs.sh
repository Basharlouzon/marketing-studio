#!/usr/bin/env bash
# Site build: pre-render the shipped SKILL.md files into static HTML pages
# and make light WebP copies of the showcase images for the landing page.
# Docs can't drift from code — this runs on every deploy (see vercel.json).
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/.pybuild${PYTHONPATH:+:$PYTHONPATH}"
need=""
python3 -c "import markdown" 2>/dev/null || need="$need markdown"
python3 -c "import PIL" 2>/dev/null || need="$need pillow"
if [ -n "$need" ]; then
  pip install $need -q --target .pybuild 2>/dev/null || pip install $need -q --break-system-packages --target .pybuild
fi
python3 scripts/md_render.py
python3 scripts/optimize_images.py
# showcase source assets are committed in docs-site/showcase/ — nothing to fetch.
echo "docs-site ready: $(ls docs-site/docs | wc -l | tr -d ' ') doc pages + landing"
