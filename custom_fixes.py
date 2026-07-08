import os
import re
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
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

# RSS 生成时要忽略的 Markdown 路径，直接在这里改
RSS_IGNORE_PATHS = [
    'docs/recom/projects/index.md',
]

load_config = lambda: tomllib.load(open(config_path, 'rb'))
read_text = lambda path: open(path, encoding='utf-8').read()


def load_hidden_slugs():
    if not os.path.exists(gitignore_path):
        return set()
    return {
        l.lstrip('/')[5:] if l.lstrip('/').startswith('docs/') else l.lstrip('/')
        for l in (
            line.strip() for line in open(gitignore_path, encoding='utf-8')
        )
        if l and not l.startswith('#') and l.endswith('.md')
    }

def load_rss_ignore_slugs():
    return {markdown_path_to_slug(p.replace('docs/', '', 1)) for p in RSS_IGNORE_PATHS if p}

def flatten_nav(nav):
    for node in nav:
        if isinstance(node, str):
            if node.endswith('.md'):
                yield node
        elif isinstance(node, list):
            yield from flatten_nav(node)
        elif isinstance(node, dict):
            for v in node.values():
                yield from flatten_nav(v)

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

def git_created_date(path):
    try:
        out = subprocess.run(['git', 'log', '--follow', '--format=%aI', '--reverse', '--', str(path)], capture_output=True, text=True, check=False).stdout.splitlines()
        return parse_iso_datetime(out[0]) if out else None
    except FileNotFoundError:
        return None

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

def resolve_pub_date(path, content):
    created = extract_created_date(content)
    first_commit = git_created_date(path)
    if created and created.astimezone(BEIJING_TZ) <= GIT_PUBDATE_CUTOFF:
        return created
    if first_commit:
        return first_commit
    return created or local_created_date(path)

parse_date_only = lambda v: (d := parse_iso_datetime(v)) and d.replace(hour=0, minute=0, second=0, microsecond=0)

def generate_rss():
    cfg = load_config().get('project', {})
    site_url, site_name, site_description = cfg.get('site_url', ''), cfg.get('site_name', 'RSS'), cfg.get('site_description', '')
    site_icon = site_url.rstrip('/') + '/assets/favicon.png' if site_url else ''
    ignore = load_hidden_slugs() | load_rss_ignore_slugs()

    def add(entries, seen, title, link, pub_date, description):
        if title and link and pub_date and link not in seen:
            seen.add(link)
            entries.append({'title': title, 'link': link, 'guid': link, 'description': description, 'pub_date': pub_date})

    entries, seen = [], set()

    for md_path in flatten_nav(cfg.get('nav', [])):
        slug = markdown_path_to_slug(md_path)
        if slug in ignore:
            continue
        p = docs_dir / md_path
        if p.exists():
            c = read_text(p)
            if not extract_rss_enabled(c):
                continue
            add(entries, seen, extract_title(c, p.stem), slug_to_url(site_url, slug), resolve_pub_date(p, c), extract_description(c))

    index_path = docs_dir / 'essays' / 'index.md'
    if index_path.exists():
        c = read_text(index_path)
        for m in re.finditer(r'\[\*\*(.+?)\*\*\]\((\./[^)]+?\.md)\)\{data-date="(\d{4}-\d{2}-\d{2})"\}', c):
            p = index_path.parent / m.group(2).lstrip('./')
            slug = markdown_path_to_slug(str(p.relative_to(docs_dir)))
            if p.exists() and slug not in ignore:
                essay_content = read_text(p)
                if not extract_rss_enabled(essay_content):
                    continue
                add(entries, seen, m.group(1).strip(), slug_to_url(site_url, slug), resolve_pub_date(p, essay_content), extract_description(essay_content))

    entries.sort(key=lambda i: (i['pub_date'], i['title']), reverse=True)

    rss_xsl_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">',
        '  <xsl:output method="html" encoding="UTF-8" indent="yes"/>',
        '  <xsl:template match="/rss">',
        '    <html lang="zh-CN">',
        '      <head>',
        '        <meta charset="UTF-8"/>',
        '        <title><xsl:value-of select="channel/title"/></title>',
        f'        <link rel="icon" href="{site_icon}"/>',
        '        <style>',
        '          body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 860px; margin: 40px auto; padding: 0 20px; line-height: 1.7; }',
        '          h1 { margin-bottom: 0.25em; }',
        '          .meta { color: #666; margin-bottom: 1.5em; }',
        '          article { padding: 1rem 0; border-bottom: 1px solid #eee; }',
        '          article:last-child { border-bottom: 0; }',
        '          a { color: inherit; text-decoration: none; }',
        '          a:hover { text-decoration: underline; }',
        '          .date { color: #666; font-size: 0.95em; }',
        '        </style>',
        '      </head>',
        '      <body>',
        '        <h1><xsl:value-of select="channel/title"/></h1>',
        '        <div class="meta"><xsl:value-of select="channel/description"/></div>',
        '        <xsl:for-each select="channel/item">',
        '          <article>',
        '            <h2><a>',
        '              <xsl:attribute name="href"><xsl:value-of select="link"/></xsl:attribute>',
        '              <xsl:value-of select="title"/>',
        '            </a></h2>',
        '            <div class="date"><xsl:value-of select="pubDate"/></div>',
        '            <xsl:if test="description">',
        '              <p><xsl:value-of select="description"/></p>',
        '            </xsl:if>',
        '          </article>',
        '        </xsl:for-each>',
        '      </body>',
        '    </html>',
        '  </xsl:template>',
        '</xsl:stylesheet>',
        ''
    ]
    rss_xsl = '\n'.join(rss_xsl_lines)

    rss_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<?xml-stylesheet type="text/xsl" href="rss.xsl"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '  <channel>', f'    <atom:link href="{escape(site_url.rstrip("/") + "/rss.xml")}" rel="self" type="application/rss+xml" />', f'    <title>{escape(site_name)}</title>', f'    <link>{escape(site_url)}</link>', f'    <description>{escape(site_description)}</description>', f'    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>']
    for i in entries:
        rss_lines += ['    <item>', f'      <title>{escape(i["title"])}</title>', f'      <link>{escape(i["link"])}</link>', f'      <guid>{escape(i["guid"])}</guid>']
        if i['description']:
            rss_lines.append(f'      <description>{escape(i["description"])}</description>')
        rss_lines += [f'      <pubDate>{format_rss_date(i["pub_date"])}</pubDate>', '    </item>']
    rss_lines += ['  </channel>', '</rss>', '']

    with open(os.path.join(site_dir, 'rss.xsl'), 'w', encoding='utf-8') as f:
        f.write(rss_xsl)
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
    generate_rss()
    activate_essays_tab()