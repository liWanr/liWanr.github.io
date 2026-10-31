import os
import json
from pathlib import Path

def search_json(path="site/search.json"):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["items"] = [
        item for item in data["items"]
        if item.get("level", 1) <= 1
    ]
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

if __name__ == '__main__':
    search_json()