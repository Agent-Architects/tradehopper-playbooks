"""Validate every SKILL.md against the Agent Skills spec, and the team knowledge bundle against OKF v0.2."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        return None, text
    block = text[4:].split("\n---\n", 1)[0]
    keys, fields = set(), {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            keys.add(m.group(1))
            fields[m.group(1)] = m.group(2).strip().strip('"')
    return (keys, fields), text


errors = []
skills = 0
for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d != ".git" and not os.path.islink(os.path.join(dirpath, d))]
    if "SKILL.md" in files:
        skills += 1
        path = os.path.join(dirpath, "SKILL.md")
        rel = os.path.relpath(path, ROOT)
        fm, text = frontmatter(path)
        if fm is None:
            errors.append(f"{rel}: no frontmatter")
            continue
        keys, f = fm
        name, desc = f.get("name", ""), f.get("description", "")
        if not NAME.match(name) or len(name) > 64:
            errors.append(f"{rel}: invalid name '{name}'")
        if name != os.path.basename(dirpath):
            errors.append(f"{rel}: name '{name}' does not match folder")
        if not 0 < len(desc) <= 1024:
            errors.append(f"{rel}: description length {len(desc)}")
        if keys - ALLOWED:
            errors.append(f"{rel}: non-standard fields {sorted(keys - ALLOWED)}")
        if text.count("\n") >= 500:
            errors.append(f"{rel}: over 500 lines")

bundle = os.path.join(ROOT, "team-pack", "template", "knowledge")
concepts = 0
for dirpath, _, files in os.walk(bundle):
    for fn in files:
        if fn.endswith(".md") and fn not in ("index.md", "log.md"):
            concepts += 1
            fm, _ = frontmatter(os.path.join(dirpath, fn))
            if fm is None or not fm[1].get("type"):
                errors.append(f"{os.path.relpath(os.path.join(dirpath, fn), ROOT)}: OKF concept without 'type'")

print(f"{skills} skills, {concepts} OKF concept files checked")
for e in errors:
    print(f"  - {e}")
sys.exit(1 if errors else 0)
