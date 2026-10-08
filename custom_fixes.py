import os
import re
import yaml

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring


def master2main():
    for r, _, fs in os.walk('site'):
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


def parse_frontmatter(path):
    content = path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL)
    return yaml.safe_load(match.group(1)) or {} if match else None


def parse_date(value):
    if isinstance(value, datetime): dt = value
    elif isinstance(value, str): dt = datetime.fromisoformat(value)
    else: return None

    return dt if dt.tzinfo else dt.replace(tzinfo=timezone(timedelta(hours=8)))


def get_posts():
    posts = []

    for root in (Path('docs/tech'), Path('docs/essays/posts')):
        if not root.exists(): continue

        for path in root.rglob('*.md'):
            try:
                meta = parse_frontmatter(path)
                if not meta: continue

                title = meta.get('title')
                date = parse_date(meta.get('date'))

                if not title or not date: continue

                relative = path.relative_to('docs')
                url = '/' + str(relative.with_suffix('')).replace('\\', '/') + '/'

                posts.append({
                    'title': str(title),
                    'date': date,
                    'url': 'https://liwanr.com' + url,
                    'description': str(meta.get('description', '')),
                })

            except Exception as e:
                print(f'Failed to process {path}: {e}')

    return posts


def generate_rss():
    posts = sorted(get_posts(), key=lambda x: x['date'], reverse=True)[:10]

    rss = Element('rss', {'version': '2.0', 'xmlns:atom': 'http://www.w3.org/2005/Atom'})
    channel = SubElement(rss, 'channel')

    SubElement(channel, 'title').text = 'liwanr.com'
    SubElement(channel, 'link').text = 'https://liwanr.com'
    SubElement(channel, 'description').text = 'liwanr.com'
    SubElement(channel, 'language').text = 'zh-CN'
    SubElement(channel, 'lastBuildDate').text = format_datetime(datetime.now(timezone(timedelta(hours=8))))

    for post in posts:
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = post['title']
        SubElement(item, 'link').text = post['url']
        SubElement(item, 'guid', {'isPermaLink': 'true'}).text = post['url']
        SubElement(item, 'pubDate').text = format_datetime(post['date'])

        if post['description']:
            SubElement(item, 'description').text = post['description']

    xml = tostring(rss, encoding='utf-8')
    Path('site/rss.xml').write_bytes(b'<?xml version="1.0" encoding="utf-8"?>\n' + xml)

    print(f'Generated site/rss.xml ({len(posts)} posts)')


if __name__ == '__main__':
    master2main()
    generate_rss()