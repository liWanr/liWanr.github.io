import os
import re
import hashlib
import subprocess
import yaml
from datetime import datetime, timedelta, timezone
from html import escape, unescape
from pathlib import Path

site_dir = 'site'
config_path = 'mkdocs.yml'
docs_dir = Path('docs')

# site/ 里这些 slug 是列表页/首页，不是文章本身，RSS 里天然要排除。
SITE_EXCLUDE_SLUGS = {'', 'about', 'blog', 'essays'}

# 手动在这里加需要从 RSS 中排除的路径。
RSS_IGNORE_SLUGS = {
    'blog/archive', 'blog/category', 'blog/page',
    'essays/archive', 'essays/category', 'essays/page',
    'about/privacy-policy', 'about/LICENSE',
}

class _ConfigLoader(yaml.SafeLoader):
    """mkdocs.yml 里的 markdown_extensions 会用 !!python/object/apply 之类的
    自定义 tag 引用 pymdownx 的函数（如 toc.slugify），我们只需要读顶层配置，
    没必要真的构造这些对象，遇到就原样忽略即可。"""

_ConfigLoader.add_multi_constructor(
    'tag:yaml.org,2002:python/', lambda loader, tag_suffix, node: None
)

def generate_rss():
    BEIJING_TZ = timezone(timedelta(hours=8))
    GIT_PUBDATE_CUTOFF = datetime(2026, 1, 26, 23, 19, tzinfo=BEIJING_TZ)
    TIME_TAG_RE = re.compile(r'<time\s+datetime="([^"]+)"')
    TITLE_TAG_RE = re.compile(r'<title>([^<]*)</title>')
    DESC_META_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)

    def read_text(path):
        with open(path, encoding='utf-8') as f:
            return f.read()

    def parse_iso_datetime_raw(v):
        """按标准 ISO 8601 语义解析：字符串里写的时区就是真实时区，正常生效。
        用于可信来源——git commit 的 author date，offset 是真实的，最终显示
        时需要真正换算成北京时间（比如 +00:00 就该老老实实 +8 小时）。"""
        v = v.strip().strip("\"'")
        if not v:
            return None
        dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
        return dt if dt.tzinfo else dt.replace(tzinfo=BEIJING_TZ)

    def parse_iso_datetime_beijing(v):
        """不管字符串里标的时区是什么，数值本身就当作北京时间，只贴标签、
        不做任何换算。用于不可信来源——HTML <time> 标签、md front matter
        里的 created 字段，这些地方的时区标注是构建时被错误写上去的。"""
        v = v.strip().strip("\"'")
        if not v:
            return None
        dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
        return dt.replace(tzinfo=BEIJING_TZ)

    def extract_title_from_html(html_content, site_name):
        m = TITLE_TAG_RE.search(html_content)
        if not m:
            return ''
        title = unescape(m.group(1)).strip()
        suffix = f' - {site_name}'
        if site_name and title.endswith(suffix):
            title = title[:-len(suffix)]
        return title

    def extract_description_from_html(html_content):
        m = DESC_META_RE.search(html_content)
        return unescape(m.group(1)).strip() if m else ''

    def build_title_to_md_index():
        # blog 插件的文章源文件平铺放在 docs/blog/posts/*.md，URL 里的年份
        # （比如 blog/2026/xxx）是插件根据文章日期在构建时现算出来塞进去的，
        # docs 源文件路径里根本没有这层年份目录，没法从 slug 反推路径。
        # 用标题去对应 docs 源文件，不受这个影响。
        index = {}
        for p in docs_dir.rglob('*.md'):
            content = read_text(p)
            parts = content.split('---', 2)
            fm = parts[1] if content.startswith('---') and len(parts) > 2 else ''
            m = re.search(r'^\s*title\s*:\s*(.+?)\s*$', fm, re.M)
            if m and m.group(1).strip().strip('"\''):
                title = m.group(1).strip().strip('"\'')
            else:
                body = parts[2] if content.startswith('---') and len(parts) > 2 else content
                hm = re.search(r'^\s*#\s+(.+?)\s*$', body, re.M)
                title = hm.group(1).strip() if hm else p.stem
            index.setdefault(title, p)
        return index

    def extract_created_date(md_path):
        if not md_path.exists():
            return None
        content = read_text(md_path)
        parts = content.split('---', 2)
        front_matter = parts[1] if content.startswith('---') and len(parts) > 2 else ''
        m = re.search(r'^\s*created\s*:\s*(.+?)\s*$', front_matter, re.M | re.I)
        return parse_iso_datetime_beijing(m.group(1)) if m else None

    def git_first_commit_date(md_path):
        if not md_path.exists():
            return None
        out = subprocess.run(
            ['git', 'log', '--follow', '--format=%aI', '--', str(md_path)],
            capture_output=True, text=True, check=False,
        ).stdout
        lines = [l for l in out.strip().splitlines() if l.strip()]
        return parse_iso_datetime_raw(lines[-1]) if lines else None

    def extract_pub_date_from_html(html_content, title, title_to_md):
        # 页面里可能有 <time datetime="2025-12-16T00:00:00+00:00"> 或
        # <time datetime="2026-06-23 00:00:00+00:00" class="md-ellipsis"> 两种写法，
        # 都只取 datetime 属性本身。HTML 里的 datetime 虽然写成 +00:00，但时间
        # 数值本身已经是北京时间，所以用 parse_iso_datetime_beijing：只贴时区
        # 标签、不做数值换算。
        m = TIME_TAG_RE.search(html_content)
        html_time = parse_iso_datetime_beijing(m.group(1)) if m else None

        md_path = title_to_md.get(title)

        # 2026-01-26 23:19 之后的时间才信 git（这个时间点之前 git 历史不可信，
        # 是迁移时批量导入产生的，不是真实的提交时间）。
        if html_time and html_time > GIT_PUBDATE_CUTOFF:
            return (git_first_commit_date(md_path) if md_path else None) or html_time

        return (extract_created_date(md_path) if md_path else None) or html_time

    def slug_to_url(site_url, slug):
        return site_url.rstrip('/') + '/' if not slug else site_url.rstrip('/') + '/' + slug.rstrip('/') + '/'

    def is_rss_ignored(slug):
        if slug in SITE_EXCLUDE_SLUGS or slug == 'recom' or slug.startswith('recom/'):
            return True
        return any(
            slug == ignore or slug.startswith(ignore.rstrip('/') + '/')
            for ignore in RSS_IGNORE_SLUGS
        )

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

    with open(config_path, encoding='utf-8') as f:
        raw_cfg = yaml.load(f, Loader=_ConfigLoader) or {}
    cfg = raw_cfg.get('project') or raw_cfg
    site_url = cfg.get('site_url', '')
    site_name = cfg.get('site_name', 'RSS')
    site_description = cfg.get('site_description', '')
    title_to_md = build_title_to_md_index()

    entries = []
    for r, dirs, fs in os.walk(site_dir):
        dirs[:] = [d for d in dirs if d not in ('assets', 'search')]
        if 'index.html' not in fs:
            continue

        html_path = Path(r) / 'index.html'
        rel_dir = html_path.relative_to(site_dir).parent.as_posix()
        slug = '' if rel_dir == '.' else rel_dir

        if is_rss_ignored(slug):
            continue

        html_content = read_text(html_path)

        title = extract_title_from_html(html_content, site_name)
        if not title:
            continue

        pub_date = extract_pub_date_from_html(html_content, title, title_to_md)
        if not pub_date:
            print(f'[skip] site/{slug}/index.html 里没有找到 <time datetime="..."> ')
            continue

        link = slug_to_url(site_url, slug)
        entries.append({
            'title': title,
            'link': link,
            'guid': hashlib.md5(link.encode()).hexdigest(),
            'description': extract_description_from_html(html_content),
            'pub_date': pub_date,
        })

    entries.sort(key=lambda i: (i['pub_date'], i['title']), reverse=True)
    entries = entries[:15]
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

def master2main():
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

if __name__ == '__main__':
    master2main()
    generate_rss()