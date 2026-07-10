import os
import re
import json
import shutil
import hashlib
import subprocess
from datetime import datetime, timedelta, timezone
from html import escape
from urllib.parse import urljoin
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

site_dir = 'site'
gitignore_path = '.gitignore'
search_json_path = os.path.join(site_dir, 'search.json')
config_path = 'zensical.toml'
docs_dir = Path('docs')


def load_config():
    with open(config_path, 'rb') as f:
        return tomllib.load(f)

def read_text(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def markdown_path_to_slug(md_path):
    slug = md_path.replace('\\', '/').strip().removeprefix('docs/').removesuffix('.md')
    return '' if slug == 'index' else slug.removesuffix('/index').rstrip('/')

slug_to_url = lambda site_url, slug: site_url.rstrip('/') + '/' if not slug else urljoin(site_url.rstrip('/') + '/', slug.rstrip('/') + '/')
front_matter = lambda content: content.split('---', 2)[1] if content.startswith('---') and len(content.split('---', 2)) > 2 else ''
parse_iso_datetime = lambda v: (datetime.fromisoformat(v.strip().strip("\"'").replace('Z', '+00:00')).astimezone(timezone.utc) if v.strip().strip("\"'") else None)

def extract_title(content, fallback):
    m = re.search(r'^\s*title\s*:\s*(.+?)\s*$', front_matter(content), re.M)
    return m.group(1).strip().strip("\"'") if m and m.group(1).strip().strip("\"'") else fallback

def extract_created_date(content):
    m = re.search(r'^(?:\s*#\s*)?(?:date\s*:\s*)?(?:craeted|created)\s*:\s*(.+?)\s*$', front_matter(content), re.M | re.I)
    return parse_iso_datetime(m.group(1)) if m else None

def extract_description(content):
    fm = front_matter(content)
    m = re.search(r'^\s*description\s*:\s*(.+?)\s*$', fm, re.M | re.I)
    if m:
        return m.group(1).strip().strip("\"'")
    return ''

def extract_rss_enabled(content):
    m = re.search(r'^\s*rss\s*:\s*(.+?)\s*$', front_matter(content), re.M | re.I)
    if not m:
        return True
    val = m.group(1).strip().strip("\"'").lower()
    return val not in {'no', 'false', 'off', '0'}

def git_first_commit(path):
    try:
        out = subprocess.run(['git', 'log', '--follow', '--raw', '--no-abbrev', '--format=%H%x00%aI', '--', str(path)], capture_output=True, text=True, check=False).stdout
    except FileNotFoundError:
        return None, None
    blocks = [b for b in out.strip().split('\n\n') if b.strip()]
    if len(blocks) < 2:
        return None, None
    head, raw = blocks[-2], blocks[-1]
    _, _, date_str = head.partition('\x00')
    m = re.search(r'^:\S+ \S+ \S+ ([0-9a-f]{40}) ', raw)
    return (m.group(1) if m else None), parse_iso_datetime(date_str)

def local_created_date(path):
    try:
        st = path.stat()
    except FileNotFoundError:
        return None
    bt = getattr(st, 'st_birthtime', None)
    if bt:
        return datetime.fromtimestamp(bt, tz=timezone.utc)
    try:
        w = subprocess.run(['stat', '-c', '%W', str(path)], capture_output=True, text=True, check=False).stdout.strip()
        return datetime.fromtimestamp(int(w), tz=timezone.utc) if w not in {'', '0', '-1'} else datetime.fromtimestamp(st.st_ctime, tz=timezone.utc)
    except (FileNotFoundError, ValueError):
        return datetime.fromtimestamp(st.st_ctime, tz=timezone.utc)

BEIJING_TZ = timezone(timedelta(hours=8))
GIT_PUBDATE_CUTOFF = datetime(2026, 1, 26, 23, 46, tzinfo=BEIJING_TZ)
format_rss_date = lambda dt: dt.astimezone(BEIJING_TZ).strftime('%a, %d %b %Y %H:%M:%S %z')

def resolve_pub_date(path, content, first_commit_date):
    created = extract_created_date(content)
    if created and created.astimezone(BEIJING_TZ) <= GIT_PUBDATE_CUTOFF:
        return created
    return first_commit_date or created or local_created_date(path)

def render_rss_item(i):
    desc = f'\n      <description>{escape(i["description"])}</description>' if i['description'] else ''
    return (
        f'    <item>\n'
        f'      <title>{escape(i["title"])}</title>\n'
        f'      <link>{escape(i["link"])}</link>\n'
        f'      <guid isPermaLink="false">{i["guid"]}</guid>{desc}\n'
        f'      <pubDate>{format_rss_date(i["pub_date"])}</pubDate>\n'
        f'    </item>'
    )

def generate_rss():
    cfg = load_config().get('project', {})
    site_url, site_name, site_description = cfg.get('site_url', ''), cfg.get('site_name', 'RSS'), cfg.get('site_description', '')

    entries = []
    for p in sorted(docs_dir.rglob('*.md')):
        if 'assets' in p.relative_to(docs_dir).parts[:-1]:
            continue
        content = read_text(p)
        if not extract_rss_enabled(content):
            continue
        title = extract_title(content, p.stem)
        blob_hash, first_commit_date = git_first_commit(p)
        pub_date = resolve_pub_date(p, content, first_commit_date)
        if not (title and pub_date):
            continue
        link = slug_to_url(site_url, markdown_path_to_slug(str(p.relative_to(docs_dir))))
        pub_second = pub_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
        guid = hashlib.md5((blob_hash or f'{pub_second}{link}').encode()).hexdigest()
        entries.append({'title': title, 'link': link, 'guid': guid, 'description': extract_description(content), 'pub_date': pub_date})

    entries.sort(key=lambda i: (i['pub_date'], i['title']), reverse=True)

    rss_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '  <channel>',
        f'    <title>{escape(site_name)}</title>',
        f'    <link>{escape(site_url)}</link>',
        f'    <description>{escape(site_description)}</description>',
        *[render_rss_item(i) for i in entries],
        '  </channel>',
        '</rss>',
        '',
    ]

    with open(os.path.join(site_dir, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rss_lines))
    print(f'RSS 已生成 {len(entries)} 条信息')

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

def process():
    for r, _, fs in os.walk(site_dir):
        for f in fs:
            if not f.endswith('.html'):
                continue

            p = os.path.join(r, f)

            with open(p, encoding='utf-8') as x:
                c = x.read()

            nc = c.replace('raw/master/docs', 'raw/main/docs')

            if nc != c:
                with open(p, 'w', encoding='utf-8') as x:
                    x.write(nc)

def hide_articles():
    if not os.path.exists(gitignore_path):
        return

    with open(gitignore_path, encoding='utf-8') as f:
        md = [l for l in (line.strip() for line in f) if l and not l.startswith('#') and l.endswith('.md')]

    if not md:
        return

    hide_slugs = [s for s in (markdown_path_to_slug(p.lstrip('/')) for p in md) if s]
    if not hide_slugs:
        return

    print('准备隐藏以下文章：')
    for slug in hide_slugs:
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

    tabs_pattern = re.compile(
        r'(<li\s+class=")(md-tabs__item)(">\s*<a\s+href="(?:\.\./)+"\s+class="md-tabs__link">[\s\S]*?Essays[\s\S]*?</a>\s*</li>)',
        re.DOTALL
    )

    nav_pattern = re.compile(
        r'(<li\s+class=")(md-nav__item)(">)\s*(<a\s+href="(?:\.\./)+"\s+class=")(md-nav__link)(">[\s\S]*?Essays[\s\S]*?</a>\s*</li>)',
        re.DOTALL
    )

    nav_replacement = r'\1\2 md-nav__item--active\3\4\5 md-nav__link--active\6'

    for r, _, fs in os.walk(essays_dir):
        if 'index.html' not in fs:
            continue

        html_path = os.path.join(r, 'index.html')
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
    generate_rss()
    activate_essays_tab()