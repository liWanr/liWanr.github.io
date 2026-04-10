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

# 2. 全局递归处理：将GitHub仓库的 master 分支替换成 main + 处理 only-dark/only-light 图片
def process_img_tags(content):
    def replace_img(m):
        tag = m.group(0)
        # 检查 class 中是否含有目标值
        cls_match = re.search(r'class=["\']([^"\']*)["\']', tag)
        if not cls_match:
            return tag
        classes = cls_match.group(1).split()
        if 'only-dark' in classes:
            hash_val = '#only-dark'
        elif 'only-light' in classes:
            hash_val = '#only-light'
        else:
            return tag
        # 给 src 末尾追加 hash，跳过已有 hash 的情况
        def add_hash(src_m):
            src_val = src_m.group(1)
            if '#only-dark' in src_val or '#only-light' in src_val:
                return src_m.group(0)
            return f'src="{src_val}{hash_val}"'
        return re.sub(r'src="([^"]*)"', add_hash, tag)

    # 只匹配 <img ... alt="..." class="only-dark/only-light" ...> 格式
    # 用非贪婪匹配，避免 base64 的长度影响整体性能
    return re.sub(r'<img\s[^>]*class=["\'][^"\']*only-(?:dark|light)[^"\']*["\'][^>]*>', replace_img, content)

for root, _, files in os.walk(site_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content

            old_str, new_str = 'raw/master/docs', 'raw/main/docs'
            if old_str in new_content:
                new_content = new_content.replace(old_str, new_str)

            new_content = process_img_tags(new_content)

            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)