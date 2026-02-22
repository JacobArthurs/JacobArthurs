import urllib.request, json, re

url = "https://api.jacobarthurs.com/blog/posts/?offset=0&limit=5"
try:
    request = urllib.request.Request(url, headers={"User-Agent": "github-actions/update-blog-posts"})
    with urllib.request.urlopen(request) as response:
        data = json.load(response)
except Exception as e:
    print(f"Failed to fetch blog posts: {e}")
    raise SystemExit(1)

items = data.get("items", [])
lines = []
for post in items:
    title = post["title"]
    slug = post["slug"]
    date = post["created_at"][:10]
    link = f"https://blog.jacobarthurs.com/post/{slug}"
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
