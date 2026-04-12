import os
import re
import shutil

site_dir = 'site'
gitignore_path = '.gitignore'

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

def process_img(content):
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

            nc = process_img(c.replace('raw/master/docs', 'raw/main/docs'))

            if nc != c:
                with open(p, 'w', encoding='utf-8') as x:
                    x.write(nc)

def hide_articles():
    if not os.path.exists(gitignore_path):
        return

    with open(gitignore_path, encoding='utf-8') as f:
        md = [
            line
            for l in f
            if (line := l.strip()) and not line.startswith('#') and line.endswith('.md')
        ]

    print('隐藏了以下文章：')
    for p in md:
        p = p.lstrip('/')

        if p.startswith('docs/'):
            p = p[5:]
        if p.endswith('.md'):
            p = p[:-3]

        t = os.path.join(site_dir, p)

        if os.path.exists(t):
            shutil.rmtree(t)
            print(f'- docs/{p}.md')
    print()

if __name__ == '__main__':
    process_index()
    process()
    hide_articles()