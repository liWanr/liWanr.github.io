import os
import re
import json
import shutil
from pathlib import Path

site_dir = 'site'
gitignore_path = '.gitignore'
search_json_path = os.path.join(site_dir, 'search.json')

def process_index():
    index_path = os.path.join(site_dir, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    pattern = (
        r'<a\s+[^>]*class=["\'][^"\']*?md-content__button\s+md-icon[^"\']*?["\'][^>]*>.*?</a>'
        r'|'
        r'<a\s+[^>]*class=["\'][^"\']*?headerlink[^"\']*?["\'][^>]*>.*?</a>'
    )

    new_index_content = re.sub(pattern, '', index_content, flags=re.DOTALL)

    new_index_content = re.sub(
        r'(<h2\b[^>]*?)\s+id="[^"]*"([^>]*>)',
        r'\1\2',
        new_index_content
    )

    new_index_content = re.sub(
        r'<h1\b[^>]*>.*?</h1>',
        '',
        new_index_content,
        flags=re.DOTALL | re.IGNORECASE
    )

    if new_index_content != index_content:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_index_content)

def process_text(content):
    def rep(m):
        tag = m.group(0)
        cls = re.search(r'class=["\']([^"\']*)["\']', tag)
        if not cls:
            return tag

        classes = cls.group(1).split()

        if 'only-dark' in classes:
            h = '#only-dark'
        elif 'only-light' in classes:
            h = '#only-light'
        else:
            return tag

        return re.sub(
            r'src="([^"]*)"',
            lambda s: f'src="{s.group(1)}{h}"' if h not in s.group(1) else s.group(0),
            tag
        )

    return re.sub(
        r'<img\s[^>]*class=["\'][^"\']*only-(?:dark|light)[^"\']*["\'][^>]*>',
        rep,
        content
    )

def process():
    for r, _, fs in os.walk(site_dir):
        for f in fs:
            if not f.endswith('.html'):
                continue

            p = os.path.join(r, f)

            with open(p, encoding='utf-8') as x:
                c = x.read()

            nc = process_text(c.replace('raw/master/docs', 'raw/main/docs'))

            if nc != c:
                with open(p, 'w', encoding='utf-8') as x:
                    x.write(nc)

def hide_articles():
    if not os.path.exists(gitignore_path):
        return

    with open(gitignore_path, encoding='utf-8') as f:
        md = []
        for l in f:
            line = l.strip()
            if line and not line.startswith('#') and line.endswith('.md'):
                md.append(line)

    if not md:
        return

    hide_slugs = []
    print('准备隐藏以下文章：')
    for p in md:
        p = p.lstrip('/')
        if p.startswith('docs/'):
            p = p[5:]
        if p.endswith('.md'):
            p = p[:-3]

        slug = p.replace('\\', '/').rstrip('/')
        hide_slugs.append(slug)
        print(f'- docs/{slug}.md')
    print()

    for slug in hide_slugs:
        t = os.path.join(site_dir, slug)
        if os.path.exists(t):
            shutil.rmtree(t, ignore_errors=True)

    if not os.path.exists(search_json_path):
        return

    with open(search_json_path, encoding='utf-8') as f:
        data = json.load(f)

    to_remove = set()
    for slug in hide_slugs:
        base = slug.rstrip('/') + '/'
        to_remove.add(base)
        to_remove.add(base + '#')

    data["items"] = [
        item for item in data.get("items", [])
        if not any(
            str(item.get("location", "")).startswith(prefix)
            for prefix in to_remove
        )
    ]

    with open(search_json_path, 'w', encoding='utf-8') as f: 
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

def activate_essays_tab():
    essays_dir = os.path.join(site_dir, 'essays')
    if not os.path.exists(essays_dir):
        return

    # 修改1: md-tabs__item 加 --active
    tabs_pattern = re.compile(
        r'(<li\s+class=")(md-tabs__item)(">\s*<a\s+href="\.\./"\s+class="md-tabs__link">[\s\S]*?Essays[\s\S]*?</a>\s*</li>)',
        re.DOTALL
    )

    # 修改2: md-nav__item 里 Essays 的链接
    nav_pattern = re.compile(
        r'(<li\s+class=")(md-nav__item)(">)\s*(<a\s+href="\.\./"\s+class=")(md-nav__link)(">[\s\S]*?Essays[\s\S]*?</a>\s*</li>)',
        re.DOTALL
    )

    nav_replacement = r'\1\2 md-nav__item--active\3\4\5 md-nav__link--active\6'

    for slug in os.listdir(essays_dir):
        slug_dir = os.path.join(essays_dir, slug)
        if not os.path.isdir(slug_dir):
            continue

        html_path = os.path.join(slug_dir, 'index.html')
        if not os.path.exists(html_path):
            continue

        with open(html_path, encoding='utf-8') as f:
            content = f.read()

        new_content = tabs_pattern.sub(r'\1\2 md-tabs__item--active\3', content)
        new_content = nav_pattern.sub(nav_replacement, new_content)

        if new_content != content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

if __name__ == '__main__':
    process_index()
    process()
    hide_articles()
    activate_essays_tab()