#!/usr/bin/env bash
# Docs build: copy the shipped SKILL.md files into the site so docs can't drift from code.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p docs-site/content
cp skills/*/SKILL.md docs-site/content/
cp skills/marketing-agent-studio/references/role-prompts.md docs-site/content/role-prompts.md
cp README.md docs-site/content/about.md
cp templates/brand-kit-template/SKILL.md docs-site/content/brand-kit-template.md
echo "docs content staged: $(ls docs-site/content | wc -l | tr -d ' ') files"
