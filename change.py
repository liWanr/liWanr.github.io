import os
import re

# 指定你的静态网站源码根目录
site_dir = 'site'

# 1. 预处理：删除根目录下 index.html 中特定的 <a> 元素
index_path = os.path.join(site_dir, 'index.html')
if os.path.exists(index_path):
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

# 3. 压缩 JS 和 CSS 文件
def minify_js(content):
    # 只合并空白和换行，不删注释，避免误伤变量名和逻辑
    content = re.sub(r'\n+', ' ', content)
    content = re.sub(r'[ \t]+', ' ', content)
    return content.strip()

def minify_css(content):
    # CSS 注释不影响逻辑，可以安全删除
    content = re.sub(r'/\*(?!!)([\s\S]*?)\*/', '', content)
    content = re.sub(r'\n+', ' ', content)
    content = re.sub(r'[ \t]+', ' ', content)
    content = re.sub(r'\s*([{}:;,>~+])\s*', r'\1', content)
    content = re.sub(r';+\}', '}', content)
    return content.strip()

for dir_path, ext, minify_fn in [
    (os.path.join(site_dir, 'assets', 'javascripts'), '.js',  minify_js),
    (os.path.join(site_dir, 'assets', 'stylesheets'), '.css', minify_css),
]:
    if not os.path.isdir(dir_path):
        continue
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(ext):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    original = f.read()
                minified = minify_fn(original)
                if minified != original:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(minified)