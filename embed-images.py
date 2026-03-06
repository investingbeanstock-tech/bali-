#!/usr/bin/env python3
"""
Run this script after placing your image files in this directory:
  - hero.jpg       → replaces the full-screen hero background
  - gallery.jpg    → replaces the bottom-right gallery photo

Usage:
  python3 embed-images.py
"""
import base64, re, sys, os

HTML_FILE = os.path.join(os.path.dirname(__file__), 'index.html')

def encode(path):
    with open(path, 'rb') as f:
        data = f.read()
    ext = path.rsplit('.', 1)[-1].lower()
    mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'
    return f'data:{mime};base64,' + base64.b64encode(data).decode()

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

changed = False

if os.path.exists('hero.jpg'):
    b64 = encode('hero.jpg')
    # Replace hero-img src (data URI)
    html, n = re.subn(
        r'(<img class="hero-img"[^>]*src=")[^"]+(")',
        lambda m: m.group(1) + b64 + m.group(2),
        html
    )
    if n:
        print(f"✓ Hero image replaced ({os.path.getsize('hero.jpg')//1024}KB)")
        changed = True
    else:
        print("✗ Could not find hero-img tag")
else:
    print("⚠ hero.jpg not found — skipping hero image")

if os.path.exists('gallery.jpg'):
    b64 = encode('gallery.jpg')
    # shot2 is the right gallery image — replace its img src
    html, n = re.subn(
        r'(<div class="g-wrap shot2">.*?<img[^>]*src=")[^"]+(")',
        lambda m: m.group(1) + b64 + m.group(2),
        html, flags=re.DOTALL
    )
    if n:
        print(f"✓ Gallery (bottom-right) image replaced ({os.path.getsize('gallery.jpg')//1024}KB)")
        # Also set object-position to keep couple centred
        html = html.replace(
            '.g-wrap.shot2 img { object-position: center 36%; }',
            '.g-wrap.shot2 img { object-position: center 38%; }'
        )
        changed = True
    else:
        print("✗ Could not find shot2 gallery tag")
else:
    print("⚠ gallery.jpg not found — skipping gallery image")

if changed:
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print("\n✓ index.html updated. Commit and push when ready.")
else:
    print("\nNo changes made.")
