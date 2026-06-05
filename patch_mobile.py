#!/usr/bin/env python3
"""Inject mobile nav into all HTML files."""
import glob
import re
import os

MOBILE_BAR = '''<div class="sidebar-overlay" id="sidebarOverlay"></div>
<header class="mobile-topbar">
  <button class="menu-btn" id="menuBtn" type="button" aria-label="Apri menu" aria-expanded="false">☰</button>
  <span class="mobile-title" id="mobileTitle">Menu</span>
</header>
'''

def depth(path):
    return path.count("/")

def asset_prefix(path):
    d = depth(path)
    return "../" * d if d else "./"

def patch_file(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    prefix = asset_prefix(path)
    css_href = f'{prefix}mobile.css'
    js_src = f'{prefix}mobile.js'

    changed = False

    if "mobile.css" not in content:
        if "</head>" in content:
            content = content.replace(
                "</head>",
                f'<link rel="stylesheet" href="{css_href}">\n</head>',
                1,
            )
            changed = True

    if 'id="menuBtn"' not in content:
        # Insert after <body> or <body ...>
        content = re.sub(
            r"(<body[^>]*>)",
            r"\1\n" + MOBILE_BAR,
            content,
            count=1,
        )
        changed = True

    if "mobile.js" not in content:
        content = content.replace(
            "</body>",
            f'<script src="{js_src}"></script>\n</body>',
            1,
        )
        changed = True

    # Remove inline sidebar hide — mobile.css handles drawer
    new_content = re.sub(
        r"\s*#sidebar\s*\{\s*display:\s*none;\s*\}",
        "",
        content,
    )
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(path, encoding="utf-8", mode="w") as f:
            f.write(content)
        return True
    return False

files = glob.glob("**/*.html", recursive=True)
files = [f for f in files if not f.startswith(".")]
ok = 0
for f in sorted(files):
    if patch_file(f):
        print("patched", f)
        ok += 1
print(f"Done: {ok}/{len(files)} files updated")
