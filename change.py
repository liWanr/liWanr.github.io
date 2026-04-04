import os
import re

# 指定你的静态网站源码根目录
site_dir = 'site'

# 1. 预处理：删除根目录下 index.html 中特定的 <a> 元素
index_path = os.path.join(site_dir, 'index.html')
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # 同时匹配 class 含有 "md-content__button md-icon" 或 "headerlink" 的 a 标签
    pattern = (
        r'<a\s+[^>]*class=["\'][^"\']*?md-content__button\s+md-icon[^"\']*?["\'][^>]*>.*?</a>'
        r'|'
        r'<a\s+[^>]*class=["\'][^"\']*?headerlink[^"\']*?["\'][^>]*>.*?</a>'
    )

    new_index_content = re.sub(pattern, '', index_content, flags=re.DOTALL)

    # 再删除 h2 标签上的 id 属性：<h2 class="no-anchor" id="..."> -> 去掉 id="..."
    new_index_content = re.sub(
    r'(<h2\b[^>]*?)\s+id="[^"]*"([^>]*>)',
        r'\1\2',
        new_index_content
    )

    # 删除所有 h1 元素（包括内容）
    new_index_content = re.sub(
        r'<h1\b[^>]*>.*?</h1>',
        '',
        new_index_content,
        flags=re.DOTALL | re.IGNORECASE
    )

    if new_index_content != index_content:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_index_content)

# 2. 全局递归处理：替换路径字符串
for root, _, files in os.walk(site_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            old_str, new_str = 'raw/master/docs', 'raw/main/docs'
            
            if old_str in content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content.replace(old_str, new_str))
                # print(f"已处理路径替换: {file_path}")

import os
import re

def minify_css(content):
    # 删除多行注释
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # 压缩空白
    content = re.sub(r'\s+', ' ', content)

    # 删除符号两边空格
    content = re.sub(r'\s*([{};:,])\s*', r'\1', content)

    return content.strip()


def minify_js(content):
    # 只删除 /* */ 注释，避免误删 URL
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # 压缩连续空白
    content = re.sub(r'\s+', ' ', content)

    # 删除常见符号两边空格
    content = re.sub(r'\s*([{};:,=+\-*/()<>])\s*', r'\1', content)

    return content.strip()


# 只处理一级目录 JS
js_dir = os.path.join(site_dir, 'assets', 'javascripts')
if os.path.exists(js_dir):
    for file in os.listdir(js_dir):
        file_path = os.path.join(js_dir, file)

        if os.path.isfile(file_path) and file.endswith('.js'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            minified = minify_js(content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(minified)


# 只处理一级目录 CSS
css_dir = os.path.join(site_dir, 'assets', 'stylesheets')
if os.path.exists(css_dir):
    for file in os.listdir(css_dir):
        file_path = os.path.join(css_dir, file)

        if os.path.isfile(file_path) and file.endswith('.css'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            minified = minify_css(content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(minified)