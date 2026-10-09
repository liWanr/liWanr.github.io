from pathlib import Path
import requests

path = Path("site/rss.xml")
old_content = path.read_bytes()

response = requests.get("https://liwanr.github.io/rss.xml", timeout=30)
response.raise_for_status()
new_content = response.content

path.write_bytes(new_content)

if old_content != path.read_bytes(): print("覆盖成功")
else: print("覆盖失败")