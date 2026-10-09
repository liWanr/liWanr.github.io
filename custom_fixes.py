import os
import json
from pathlib import Path

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
    master2main()
    search_json()