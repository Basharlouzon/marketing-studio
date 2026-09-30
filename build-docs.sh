#!/usr/bin/env bash
# Docs build: copy the shipped SKILL.md files into the site so docs can't drift from code.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p docs-site/content
for skill in inspiration-intake mbk-brand-kit social-image-studio marketing-agent-studio remotion-motion-studio; do
  cp "skills/${skill}/SKILL.md" "docs-site/content/${skill}.md"
done
cp skills/marketing-agent-studio/references/role-prompts.md docs-site/content/role-prompts.md
cp README.md docs-site/content/about.md
cp templates/brand-kit-template/SKILL.md docs-site/content/brand-kit-template.md
echo "docs content staged: $(ls docs-site/content | wc -l | tr -d ' ') files"
