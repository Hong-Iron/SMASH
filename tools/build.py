# Builds site/index.html from src/index.html and schools.json.
# usage: python3 tools/build.py
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src" / "index.html").read_text(encoding="utf-8")
schools = json.loads((root / "schools.json").read_text(encoding="utf-8"))
assert "__SCHOOLS__" in tpl
out = tpl.replace("__SCHOOLS__", json.dumps(schools, ensure_ascii=False).replace("</", "<\\/"))
(root / "site" / "index.html").write_text(out, encoding="utf-8")
print("site/index.html", len(out.encode()) // 1024, "KB,", len(schools), "schools")
