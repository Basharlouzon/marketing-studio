#!/usr/bin/env bash
# Marketing Studio — idempotent installer. Copies the 5 skills into your agent's skills folder.
#   ZCode (default):  ./install.sh
#   Claude Code:      SKILLS_DIR=~/.claude/skills ./install.sh
# Safe to run from any directory and to re-run (it replaces only these 5 skill folders).
set -euo pipefail
DEST="${SKILLS_DIR:-${HOME}/.zcode/skills}"
SRC="$(cd "$(dirname "$0")" && pwd)/skills"

echo "Installing Marketing Studio skills → ${DEST}"
mkdir -p "${DEST}"
for skill in inspiration-intake mbk-brand-kit social-image-studio marketing-agent-studio remotion-motion-studio; do
  if [ -d "${SRC}/${skill}" ]; then
    rm -rf "${DEST:?}/${skill}"
    cp -R "${SRC}/${skill}" "${DEST}/${skill}"
    rm -rf "${DEST}/${skill}/scripts/__pycache__" 2>/dev/null || true
    echo "  ✓ ${skill}"
  else
    echo "  ✗ missing ${SRC}/${skill}" >&2
    exit 1
  fi
done
chmod +x "${DEST}/remotion-motion-studio/scripts/extract_qa_frames.sh" 2>/dev/null || true
chmod +x "${DEST}/social-image-studio/scripts/preverify.py" 2>/dev/null || true
echo ""
echo "Done. Next:"
echo "  1. Restart your agent (ZCode or Claude Code) so it loads the skills."
echo "  2. Ask: Make 12 Instagram posts for <your product> for December."
