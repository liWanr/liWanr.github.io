import os
import re
import json
import shutil
import hashlib
import subprocess
import yaml
from datetime import datetime, timedelta, timezone
from html import escape, unescape
from pathlib import Path

site_dir = 'site'
gitignore_path = '.gitignore'
search_json_path = os.path.join(site_dir, 'search.json')
config_path = 'mkdocs.yml'
docs_dir = Path('docs')


def load_config():
    with open(config_path, encoding='utf-8') as f:
        return yaml.unsafe_load(f)

def read_text(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def markdown_path_to_slug(md_path):
    slug = md_path.replace('\\', '/').strip().removeprefix('docs/').removesuffix('.md')
    return '' if slug == 'index' else slug.removesuffix('/index').rstrip('/')

BEIJING_TZ = timezone(timedelta(hours=8))
GIT_PUBDATE_CUTOFF = datetime(2026, 1, 26, 23, 19, tzinfo=BEIJING_TZ)
format_rss_date = lambda dt: dt.astimezone(BEIJING_TZ).strftime('%a, %d %b %Y %H:%M:%S %z')

def parse_iso_datetime(v):
    v = v.strip().strip("\"'")
    if not v:
        return None
    dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
    return dt if dt.tzinfo else dt.replace(tzinfo=BEIJING_TZ)

front_matter = lambda content: content.split('---', 2)[1] if content.startswith('---') and len(content.split('---', 2)) > 2 else ''

def extract_created_date(content):
    m = re.search(r'^\s*created\s*:\s*(.+?)\s*$', front_matter(content), re.M | re.I)
    return parse_iso_datetime(m.group(1)) if m else None

def git_first_commit_date(path):
    try:
        out = subprocess.run(
            ['git', 'log', '--follow', '--format=%aI', '--', str(path)],
            capture_output=True, text=True, check=False,
        ).stdout
    except FileNotFoundError:
        return None
    lines = [l for l in out.strip().splitlines() if l.strip()]
    return parse_iso_datetime(lines[-1]) if lines else None

def local_created_date(path):
    st = path.stat()
    bt = getattr(st, 'st_birthtime', None)
    if bt:
        return datetime.fromtimestamp(bt, tz=timezone.utc)
    try:
        w = subprocess.run(['stat', '-c', '%W', str(path)], capture_output=True, text=True, check=False).stdout.strip()
        return datetime.fromtimestamp(int(w), tz=timezone.utc) if w not in {'', '0', '-1'} else datetime.fromtimestamp(st.st_ctime, tz=timezone.utc)
    except (FileNotFoundError, ValueError):
        return datetime.fromtimestamp(st.st_ctime, tz=timezone.utc)

def resolve_pub_date(md_path):
    content = read_text(md_path)
    created = extract_created_date(content)
    if created and created.astimezone(BEIJING_TZ) <= GIT_PUBDATE_CUTOFF:
        return created
    return git_first_commit_date(md_path) or created or local_created_date(md_path)

def strip_front_matter(content):
    parts = content.split('---', 2)
    return parts[2] if content.startswith('---') and len(parts) > 2 else content

def extract_title_from_markdown(content):
    m = re.search(r'^\s*title\s*:\s*(.+?)\s*$', front_matter(content), re.M)
    if m:
        t = m.group(1).strip().strip("\"'")
        if t:
            return t
    m = re.search(r'^\s*#\s+(.+?)\s*$', strip_front_matter(content), re.M)
    return m.group(1).strip() if m else None

def build_title_index():
    index = {}
    for p in docs_dir.rglob('*.md'):
        title = extract_title_from_markdown(read_text(p))
        if title:
            index.setdefault(title, p)
    return index

_TIME_RE = re.compile(r'<time\b[^>]*?\bdatetime="([^"]+)"')
_TITLE_RE = re.compile(r'<title>([^<]*)</title>')
_DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
_OG_DESC_RE = re.compile(r'<meta\s+property="og:description"\s+content="([^"]*)"')

_EXCLUDE_EXACT = {'blog'}
_EXCLUDE_PREFIXES = ('blog/archive', 'blog/category', 'blog/categories', 'blog/tag', 'blog/tags', 'blog/page', 'recom', 'about')


def find_site_pages():
    for r, dirs, fs in os.walk(site_dir):
        dirs[:] = [d for d in dirs if d not in ('assets', 'search')]
        if 'index.html' in fs:
            yield os.path.join(r, 'index.html')

def is_excluded_page(html_path):
    rel_dir = Path(html_path).relative_to(site_dir).parent.as_posix()
    if rel_dir in _EXCLUDE_EXACT:
        return True
    return any(rel_dir == p or rel_dir.startswith(p + '/') for p in _EXCLUDE_PREFIXES)

def html_link(html_path, site_url):
    rel_dir = Path(html_path).relative_to(site_dir).parent.as_posix()
    return site_url.rstrip('/') + '/' if rel_dir == '.' else f"{site_url.rstrip('/')}/{rel_dir}/"

def extract_title(html, site_name):
    m = _TITLE_RE.search(html)
    if not m:
        return ''
    title = unescape(m.group(1)).strip()
    suffix = f' - {site_name}'
    return title[:-len(suffix)] if site_name and title.endswith(suffix) else title

def extract_description(html):
    m = _DESC_RE.search(html) or _OG_DESC_RE.search(html)
    return unescape(m.group(1)).strip() if m else ''

def has_pub_time(html):
    return bool(_TIME_RE.search(html))

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
    cfg = load_config()
    site_url = cfg.get('site_url', '')
    site_name = cfg.get('site_name', 'RSS')
    site_description = cfg.get('site_description', '')
    title_index = build_title_index()

    entries = []
    for html_path in sorted(find_site_pages()):
        rel = os.path.relpath(html_path, site_dir)
        if is_excluded_page(html_path):
            print(f'[skip] {rel}: 命中排除路径（blog 归档/分类/标签/分页、recom）')
            continue
        html = read_text(html_path)
        if not has_pub_time(html):
            print(f'[skip] {rel}: 页面里没有 <time> 元素')
            continue
        title = extract_title(html, site_name)
        if not title:
            print(f'[skip] {rel}: 拿不到 <title>')
            continue
        md_path = title_index.get(title)
        if not md_path:
            print(f'[skip] {rel}: 按标题 "{title}" 反查不到 docs/ 源文件')
            continue
        pub_date = resolve_pub_date(md_path)
        if not pub_date:
            print(f'[skip] {rel}: 源文件 {md_path} 拿不到任何日期')
            continue
        link = html_link(html_path, site_url)
        entries.append({
            'title': title,
            'link': link,
            'guid': hashlib.md5(link.encode()).hexdigest(),
            'description': extract_description(html),
            'pub_date': pub_date,
        })

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
        r'(<li\s+class=")(md-tabs__item)(">\s*<a\s+href="(?:\.\./)+"\s+class="md-tabs__link">[\s\S]*?ESSAYS[\s\S]*?</a>\s*</li>)',
        re.DOTALL
    )

    nav_pattern = re.compile(
        r'(<li\s+class=")(md-nav__item)(">)\s*(<a\s+href="(?:\.\./)+"\s+class=")(md-nav__link)(">[\s\S]*?ESSAYS[\s\S]*?</a>\s*</li>)',
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
    activate_essays_tab()
    generate_rss()