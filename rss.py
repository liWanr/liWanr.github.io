from pathlib import Path
import requests


response = requests.get("https://liwanr.github.io/rss.xml", timeout=30)
response.raise_for_status()
Path("site/rss.xml").write_bytes(response.content)