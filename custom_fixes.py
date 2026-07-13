import os
import re
import json
import shutil
import hashlib
import subprocess
try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib
from datetime import datetime, timedelta, timezone
from html import escape, unescape
from pathlib import Path

site_dir = 'site'
gitignore_path = '.gitignore'
search_json_path = os.path.join(site_dir, 'search.json')
config_path = 'zensical.toml'
docs_dir = Path('docs')


def markdown_path_to_slug(md_path):
    slug = md_path.replace('\\', '/').strip().removeprefix('docs/').removesuffix('.md')
    return '' if slug == 'index' else slug.removesuffix('/index').rstrip('/')

def generate_rss():
    EXCLUDE_DOCS = {'index.md', 'about.md', 'blog/index.md', 'essays/index.md'}
    BEIJING_TZ = timezone(timedelta(hours=8))
    GIT_PUBDATE_CUTOFF = datetime(2026, 1, 26, 23, 19, tzinfo=BEIJING_TZ)

    def read_text(path):
        with open(path, encoding='utf-8') as f:
            return f.read()

    def parse_iso_datetime(v):
        v = v.strip().strip("\"'")
        if not v:
            return None
        dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
        return dt if dt.tzinfo else dt.replace(tzinfo=BEIJING_TZ)

    def front_matter(content):
        parts = content.split('---', 2)
        return parts[1] if content.startswith('---') and len(parts) > 2 else ''

    def strip_front_matter(content):
        parts = content.split('---', 2)
        return parts[2] if content.startswith('---') and len(parts) > 2 else content

    def extract_created_date(content):
        m = re.search(r'^\s*created\s*:\s*(.+?)\s*$', front_matter(content), re.M | re.I)
        return parse_iso_datetime(m.group(1)) if m else None

    def extract_title(content, fallback):
        m = re.search(r'^\s*title\s*:\s*(.+?)\s*$', front_matter(content), re.M)
        if m:
            t = m.group(1).strip().strip("\"'")
            if t:
                return t
        m = re.search(r'^\s*#\s+(.+?)\s*$', strip_front_matter(content), re.M)
        return m.group(1).strip() if m else fallback

    def extract_description(content):
        m = re.search(r'^\s*description\s*:\s*(.+?)\s*$', front_matter(content), re.M | re.I)
        return m.group(1).strip().strip("\"'") if m else ''

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

    def resolve_pub_date(md_path, content):
        created = extract_created_date(content)
        if created and created.astimezone(BEIJING_TZ) <= GIT_PUBDATE_CUTOFF:
            return created
        return git_first_commit_date(md_path) or created or local_created_date(md_path)

    def is_excluded_doc(rel_path):
        return rel_path in EXCLUDE_DOCS or rel_path.startswith('recom/')

    def slug_to_url(site_url, slug):
        return site_url.rstrip('/') + '/' if not slug else site_url.rstrip('/') + '/' + slug.rstrip('/') + '/'

    def build_site_link_index(site_name):
        """标题 -> site/ 里对应页面所在目录，用来反查被 blog 插件按年月重新分配路径的文章。"""
        title_re = re.compile(r'<title>([^<]*)</title>')
        index = {}
        for r, dirs, fs in os.walk(site_dir):
            dirs[:] = [d for d in dirs if d not in ('assets', 'search')]
            if 'index.html' not in fs:
                continue
            html_path = os.path.join(r, 'index.html')
            m = title_re.search(read_text(html_path))
            if not m:
                continue
            title = unescape(m.group(1)).strip()
            suffix = f' - {site_name}'
            if site_name and title.endswith(suffix):
                title = title[:-len(suffix)]
            index.setdefault(title, html_path)
        return index

    def render_rss_item(i):
        desc = f'\n      <description>{escape(i["description"])}</description>' if i['description'] else ''
        pub_date = i['pub_date'].astimezone(BEIJING_TZ).strftime('%a, %d %b %Y %H:%M:%S %z')
        return (
            f'    <item>\n'
            f'      <title>{escape(i["title"])}</title>\n'
            f'      <link>{escape(i["link"])}</link>\n'
            f'      <guid isPermaLink="false">{i["guid"]}</guid>{desc}\n'
            f'      <pubDate>{pub_date}</pubDate>\n'
            f'    </item>'
        )

    with open(config_path, 'rb') as f:
        cfg = tomllib.load(f).get('project', {})
    site_url = cfg.get('site_url', '')
    site_name = cfg.get('site_name', 'RSS')
    site_description = cfg.get('site_description', '')
    site_link_index = build_site_link_index(site_name)

    entries = []
    for p in sorted(docs_dir.rglob('*.md')):
        rel_path = p.relative_to(docs_dir).as_posix()
        if 'assets' in p.relative_to(docs_dir).parts[:-1]:
            continue
        if is_excluded_doc(rel_path):
            continue

        content = read_text(p)
        title = extract_title(content, p.stem)
        pub_date = resolve_pub_date(p, content)
        if not (title and pub_date):
            continue

        if rel_path.startswith('blog/'):
            html_path = site_link_index.get(title)
            if not html_path:
                print(f'[skip] docs/{rel_path}: 按标题 "{title}" 在 site/ 里反查不到对应页面')
                continue
            rel_dir = Path(html_path).relative_to(site_dir).parent.as_posix()
            link = slug_to_url(site_url, rel_dir)
        else:
            link = slug_to_url(site_url, markdown_path_to_slug(str(p.relative_to(docs_dir))))

        entries.append({
            'title': title,
            'link': link,
            'guid': hashlib.md5(link.encode()).hexdigest(),
            'description': extract_description(content),
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

def flatten_blog_posts_path():
    posts_dir = os.path.join(site_dir, 'blog', 'posts')
    if not os.path.isdir(posts_dir):
        return

    blog_dir = os.path.join(site_dir, 'blog')
    for name in os.listdir(posts_dir):
        src = os.path.join(posts_dir, name)
        dst = os.path.join(blog_dir, name)
        if os.path.exists(dst):
            shutil.rmtree(dst) if os.path.isdir(dst) else os.remove(dst)
        shutil.move(src, dst)
    shutil.rmtree(posts_dir, ignore_errors=True)

    for r, _, fs in os.walk(site_dir):
        for f in fs:
            if not f.endswith(('.html', '.xml', '.json')):
                continue

            p = os.path.join(r, f)

            with open(p, encoding='utf-8') as x:
                c = x.read()

            nc = c.replace('/blog/posts/', '/blog/')

            if nc != c:
                with open(p, 'w', encoding='utf-8') as x:
                    x.write(nc)

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
    flatten_blog_posts_path()
    process()
    hide_articles()
    activate_essays_tab()
    generate_rss()