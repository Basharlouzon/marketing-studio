p = "scripts/md_render.py"
s = open(p).read()

# 1. site URL constant
s = s.replace(
    'REPO = "https://github.com/Basharlouzon/marketing-studio"',
    'REPO = "https://github.com/Basharlouzon/marketing-studio"\nSITE_URL = "https://marketing-studio-basharlouzons-projects.vercel.app"',
)
assert "SITE_URL" in s, "anchor 1 failed"

# 2. og:image + og:url in template head
old = '<meta property="og:type" content="article" />\n<meta property="og:site_name" content="Marketing Studio" />'
new = ('<meta property="og:type" content="article" />\n'
       '<meta property="og:site_name" content="Marketing Studio" />\n'
       '<meta property="og:image" content="{og_image}" />\n'
       '<meta property="og:url" content="{og_url}" />')
assert old in s, "anchor 2 failed"
s = s.replace(old, new)

# 3. date stamp in the src line (match on the stable tail, not the apostrophe)
old_src = 'can'
s = s.replace(
    "— docs can't drift from the code.</p>",
    "— docs can't drift from the code. <span class=\"mono\">Last built {date}</span></p>",
)

# 4. prev/next block
old_body = "    {body}\n  </main>"
new_body = ("    {body}\n\n"
            "    <nav class=\"pager\" aria-label=\"Adjacent pages\">\n"
            "      {pager_prev}\n"
            "      {pager_next}\n"
            "    </nav>\n  </main>")
assert old_body in s, "anchor 4 failed"
s = s.replace(old_body, new_body)

# 5. build_page: compute og/prev/next/date and pass to template
old_ret = "    src_rel = src.relative_to(ROOT).as_posix()\n\n    return PAGE_TMPL.format("
new_ret = '''    src_rel = src.relative_to(ROOT).as_posix()

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
        date=built,'''
assert old_ret in s, "anchor 5 failed"
s = s.replace(old_ret, new_ret)

open(p, "w").write(s)
print("md_render.py enhanced: SITE_URL, og:image, date stamp, prev/next")
