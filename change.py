import os
import re

# 指定你的静态网站源码根目录
site_dir = 'site'

# 1. 预处理：删除根目录下 index.html 中特定的 <a> 元素
index_path = os.path.join(site_dir, 'index.html')
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # 正则匹配特定的 <a> 标签及其内容并删除
    # 匹配模式：<a ... class="md-content__button md-icon" ...> ... </a>
    pattern = r'<a\s+[^>]*class=["\']md-content__button\s+md-icon["\'][^>]*>.*?</a>'
    new_index_content = re.sub(pattern, '', index_content, flags=re.DOTALL)
    
    if new_index_content != index_content:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_index_content)
        # print(f"已清理根目录 index.html 中的特定按钮。")

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