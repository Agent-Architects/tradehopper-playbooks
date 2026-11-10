"""Check the HTML docs: balanced tags, every in-page anchor resolves, every repo path in <code> exists."""
import html.parser
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = ["A-security-pack.html", "B-team-orchestration-pack.html"]
VOID = {"meta", "br", "img", "link", "input", "hr", "wbr", "source"}
# Paths in docs that refer to this repo and must exist here.
REPO_PATH = re.compile(r"^(security-pack|team-pack|\.claude/skills)/[^\s<>*]+$")


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.ids, self.anchors, self.codes, self.errors = [], set(), [], [], []
        self._in_code = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href", "").startswith("#"):
            self.anchors.append(a["href"][1:])
        if tag == "code":
            self._in_code = True
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "code":
            self._in_code = False
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"unexpected </{tag}> (open: {self.stack[-3:]})")

    def handle_data(self, data):
        if self._in_code:
            self.codes.append(data.strip())


failed = False
for doc in DOCS:
    p = Parser()
    p.feed(open(os.path.join(ROOT, doc), encoding="utf-8").read())
    problems = list(p.errors)
    if p.stack:
        problems.append(f"unclosed tags: {p.stack}")
    problems += [f"missing anchor #{a}" for a in p.anchors if a not in p.ids]
    for c in p.codes:
        if REPO_PATH.match(c) and "<" not in c:
            target = os.path.join(ROOT, c.rstrip("/"))
            if not os.path.exists(target):
                problems.append(f"referenced path not found: {c}")
    print(f"{doc}: {len(p.anchors)} anchors, {'OK' if not problems else 'FAIL'}")
    for pr in problems:
        print(f"  - {pr}")
    failed |= bool(problems)
sys.exit(1 if failed else 0)
