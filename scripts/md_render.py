#!/usr/bin/env python3
"""Pre-render the Marketing Studio docs into static, JS-free HTML pages.

Reads the shipped SKILL.md files (plus README + role-prompts) straight from
the repo and writes full HTML pages into docs-site/docs/<name>.html, wrapped
in the shared light chrome (nav, sidebar, right-hand TOC, footer). Docs can
never drift from the code: the site build re-renders them every deploy.

The DOCS registry below is the single source of truth for the doc list —
every sidebar, the TOC, and the page set are generated from it.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs-site"
OUT = SITE / "docs"
REPO = "https://github.com/Basharlouzon/marketing-studio"
SITE_URL = "https://marketing-studio-basharlouzons-projects.vercel.app"

# (page id, display label, source file) — single source for nav + pages
DOCS = [
    ("about", "About", ROOT / "README.md"),
    ("inspiration-intake", "inspiration-intake", ROOT / "skills/inspiration-intake/SKILL.md"),
    ("mbk-brand-kit", "brand-kit", ROOT / "skills/mbk-brand-kit/SKILL.md"),
    ("social-image-studio", "social-image-studio", ROOT / "skills/social-image-studio/SKILL.md"),
    ("marketing-agent-studio", "marketing-agent-studio", ROOT / "skills/marketing-agent-studio/SKILL.md"),
    ("remotion-motion-studio", "remotion-motion-studio", ROOT / "skills/remotion-motion-studio/SKILL.md"),
    ("brand-kit-template", "brand-kit template", ROOT / "templates/brand-kit-template/SKILL.md"),
    ("role-prompts", "agent role prompts", ROOT / "skills/marketing-agent-studio/references/role-prompts.md"),
]

# Sidebar labels keep the numbered studio order
SIDEBAR_LABELS = {
    "about": "About",
    "inspiration-intake": "0 · inspiration-intake",
    "mbk-brand-kit": "1 · brand-kit",
    "social-image-studio": "2 · social-image-studio",
    "marketing-agent-studio": "3 · marketing-agent-studio",
    "remotion-motion-studio": "4 · remotion-motion-studio",
    "brand-kit-template": "+ · brand-kit template",
    "role-prompts": "· agent role prompts",
}


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


# the README ships a placeholder clone URL — docs pages get the real one
CLONE_CMD = f"git clone {REPO}.git"


def rewrite_placeholders(text: str) -> str:
    return text.replace("git clone <this-repo>", CLONE_CMD)


def escape_stray_lt(text: str) -> str:
    """Escape raw `<` outside fenced code blocks and inline code spans.

    Legitimate inline HTML (real tags) survives; stray angle brackets like
    `<app>` in prose become visible text instead of silently vanishing.
    """
    out: list[str] = []
    in_fence = False
    fence_re = re.compile(r"^\s*(```|~~~)")
    code_span = re.compile(r"(`+[^`]*`+)")
    for line in text.splitlines(keepends=True):
        if fence_re.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        nl = line.endswith("\n")
        body = line[:-1] if nl else line
        parts = code_span.split(body)
        for i, part in enumerate(parts):
            if i % 2 == 1:  # inside a `code span`
                continue
            parts[i] = re.sub(r"<(?![a-zA-Z/!?])", "&lt;", part)
        out.append("".join(parts) + ("\n" if nl else ""))
    return "".join(out)


def render_markdown(text: str) -> str:
    text = strip_frontmatter(text)
    text = rewrite_placeholders(text)
    text = escape_stray_lt(text)
    return markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )


def postprocess(body: str) -> str:
    # wrap tables for horizontal scroll on small screens
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    body = body.replace("</table>", "</table></div>")

    # copy button on every code block
    body = body.replace(
        "<pre>",
        '<div class="codeblock"><button class="copy-btn" type="button">Copy</button><pre>',
    )
    body = body.replace("</pre>", "</pre></div>")

    # hover anchor on every h2
    def anchor(m: re.Match) -> str:
        hid, inner = m.group(1), m.group(2)
        return (
            f'<h2 id="{hid}">{inner}'
            f'<a class="anchor" href="#{hid}" aria-label="Link to this section">#</a></h2>'
        )

    body = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', anchor, body, flags=re.S)

    # rewrite repo-relative links to GitHub (links may point at .md files,
    # which GitHub renders — so the docs stay navigable without the site)
    body = re.sub(
        r'href="(skills/[^"]+|templates/[^"]+)"',
        rf'href="{REPO}/blob/main/\1"',
        body,
    )
    return body


def extract_toc(body: str) -> list[tuple[str, str]]:
    toc = []
    for hid, inner in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S):
        inner = re.sub(r'<a class="anchor"[^>]*>.*?</a>', "", inner, flags=re.S)
        title = re.sub(r"<[^>]+>", "", inner)
        toc.append((hid, html.unescape(title).strip()))
    return toc


def first_paragraph_text(body: str, limit: int = 160) -> str:
    m = re.search(r"<p>(.*?)</p>", body, flags=re.S)
    if not m:
        return "Marketing Studio documentation."
    text = re.sub(r"<[^>]+>", "", m.group(1))
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text[: limit - 1].rstrip() + ("…" if len(text) > limit else "")


PAGE_TMPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} — Marketing Studio Docs</title>
<meta name="description" content="{description}" />
<meta name="theme-color" content="#fbfcfe" />
<link rel="icon" type="image/svg+xml" href="../favicon.svg" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Marketing Studio" />
<meta property="og:image" content="{og_image}" />
<meta property="og:url" content="{og_url}" />
<meta property="og:title" content="{title} — Marketing Studio Docs" />
<meta property="og:description" content="{description}" />
<meta name="twitter:card" content="summary" />
<meta name="twitter:title" content="{title} — Marketing Studio Docs" />
<meta name="twitter:description" content="{description}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../styles.css" />
</head>
<body class="docs-body">
<a class="skip" href="#doc">Skip to content</a>

<header class="nav docs-nav">
  <div class="wrap nav-inner">
    <a class="brand" href="../index.html"><span class="mark" aria-hidden="true">MS</span> Marketing Studio</a>
    <nav class="nav-links" aria-label="Primary">
      <a href="../index.html#skills">Skills</a>
      <a href="../index.html#showcase">Showcase</a>
      <a href="about.html">Docs</a>
      <a class="btn btn-gold" href="../index.html#install">Get the skills</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="sidebar" aria-label="Open docs menu">
        <svg width="18" height="14" viewBox="0 0 18 14" fill="none" aria-hidden="true">
          <path d="M1 1h16M1 7h16M1 13h16" stroke="#101b37" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
      </button>
    </nav>
  </div>
</header>

<button class="scrim" id="scrim" tabindex="-1" aria-hidden="true"></button>

<div class="docs-shell">
  <aside class="sidebar" id="sidebar" aria-label="Docs">
    <p class="side-label">Docs</p>
    <nav class="side-list">
      {sidebar}
    </nav>
    <div class="side-sep" role="presentation"></div>
    <nav class="side-list">
      <a href="../index.html">← Back to home</a>
      <a href="{repo}" target="_blank" rel="noopener">GitHub repo ↗</a>
    </nav>
  </aside>

  <main class="doc" id="doc">
    <header class="doc-head">
      <p class="eyebrow">Marketing Studio docs</p>
      <h1>{title}</h1>
      <p class="src">Pre-rendered at build from <a href="{src_url}" target="_blank" rel="noopener"><code>{src_path}</code></a> — docs can't drift from the code. <span class="mono">Last built {date}</span></p>
    </header>
    {body}

    <nav class="pager" aria-label="Adjacent pages">
      {pager_prev}
      {pager_next}
    </nav>
  </main>

  <aside class="toc" aria-label="On this page">
    <p class="toc-label">On this page</p>
    <ul>
      {toc}
    </ul>
  </aside>
</div>

<footer class="docs-footer">
  <b>Marketing Studio</b> · docs are pre-rendered from the shipped SKILL.md files at build time — they can't drift from the code · <span style="font-family: var(--mono); font-size: 12px;">v1.0</span>
</footer>

<script src="../app.js"></script>
</body>
</html>
"""


def build_page(doc_id: str, title: str, src: Path, active_id: str) -> str:
    raw = src.read_text(encoding="utf-8")
    body = postprocess(render_markdown(raw))
    toc_items = extract_toc(body)

    sidebar_items = []
    for pid, label, _ in DOCS:
        active = ' class="active" aria-current="page"' if pid == active_id else ""
        sidebar_items.append(f'<a href="{pid}.html"{active}>{html.escape(SIDEBAR_LABELS[pid])}</a>')
    toc_items_html = "\n".join(
        f'<li><a href="#{hid}">{html.escape(t)}</a></li>' for hid, t in toc_items
    )
    src_rel = src.relative_to(ROOT).as_posix()

    idx = next(i for i, (pid, _, _) in enumerate(DOCS) if pid == active_id)
    prev_item = DOCS[idx - 1] if idx > 0 else None
    next_item = DOCS[idx + 1] if idx + 1 < len(DOCS) else None
    pager_prev = (
        f'<a class="pager-link prev" href="{prev_item[0]}.html"><span>← Previous</span><b>{SIDEBAR_LABELS[prev_item[0]]}</b></a>'
        if prev_item else "<span></span>"
    )
    pager_next = (
        f'<a class="pager-link next" href="{next_item[0]}.html"><span>Next →</span><b>{SIDEBAR_LABELS[next_item[0]]}</b></a>'
        if next_item else "<span></span>"
    )

    from datetime import date
    built = date.today().isoformat()

    return PAGE_TMPL.format(
        og_image=f"{SITE_URL}/og-image.png",
        og_url=f"{SITE_URL}/docs/{doc_id}.html",
        date=built,
        pager_prev=pager_prev,
        pager_next=pager_next,
        title=html.escape(title),
        description=html.escape(first_paragraph_text(body)),
        sidebar="\n      ".join(sidebar_items),
        toc=toc_items_html or '<li style="color: var(--txt-l-muted); padding-left: 14px;">—</li>',
        body=body,
        src_path=html.escape(src_rel),
        src_url=f"{REPO}/blob/main/{src_rel}",
        repo=REPO,
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for doc_id, title, src in DOCS:
        if not src.exists():
            print(f"ERROR: missing source {src}", file=sys.stderr)
            return 1
        page = build_page(doc_id, title, src, active_id=doc_id)
        target = OUT / f"{doc_id}.html"
        target.write_text(page, encoding="utf-8")
        n_h2 = len(extract_toc(page))
        print(f"  docs/{doc_id}.html  ({n_h2} sections, {len(page):,} bytes)")
    print(f"OK: {len(DOCS)} doc pages written to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
