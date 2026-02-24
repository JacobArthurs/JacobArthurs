import urllib.request, re
from xml.etree import ElementTree
from email.utils import parsedate_to_datetime

url = "https://blog.jacobarthurs.com/rss.xml"
try:
    with urllib.request.urlopen(url) as response:
        tree = ElementTree.parse(response)
except Exception as e:
    print(f"Failed to fetch RSS feed: {e}")
    raise SystemExit(1)

items = tree.findall(".//item")[:5]
lines = []
for item in items:
    title = item.find("title").text
    link = item.find("link").text
    date = parsedate_to_datetime(item.find("pubDate").text).strftime("%Y-%m-%d")
    lines.append(f"- [{title}]({link}) — {date}")

new_block = "<!-- BLOG-POSTS:START -->\n" + "\n".join(lines) + "\n<!-- BLOG-POSTS:END -->"

with open("README.md", "r") as f:
    content = f.read()

updated = re.sub(
    r"<!-- BLOG-POSTS:START -->.*?<!-- BLOG-POSTS:END -->",
    new_block,
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(updated)

print("Done.")