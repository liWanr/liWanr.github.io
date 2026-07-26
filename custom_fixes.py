import os
import re
import hashlib
import subprocess
import yaml
from datetime import datetime, timedelta, timezone
from html import escape, unescape
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

if __name__ == '__main__':
    master2main()