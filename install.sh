#!/usr/bin/env bash
# Marketing Studio — idempotent installer. Copies the 5 skills into ~/.zcode/skills/.
set -euo pipefail
DEST="${HOME}/.zcode/skills"
SRC="$(cd "$(dirname "$0")" && pwd)/skills"

echo "Installing Marketing Studio skills → ${DEST}"
for skill in inspiration-intake mbk-brand-kit social-image-studio marketing-agent-studio remotion-motion-studio; do
  if [ -d "${SRC}/${skill}" ]; then
    rm -rf "${DEST}/${skill}"
    cp -R "${SRC}/${skill}" "${DEST}/${skill}"
    echo "  ✓ ${skill}"
  else
    echo "  ✗ missing ${SRC}/${skill}" >&2
    exit 1
  fi
done
chmod +x "${DEST}/remotion-motion-studio/scripts/extract_qa_frames.sh" 2>/dev/null || true
chmod +x "${DEST}/social-image-studio/scripts/preverify.py" 2>/dev/null || true
echo "Done. Restart ZCode so the skills are discovered."
