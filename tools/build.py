# Builds site/index.html from src/index.html, schools.json and config.json.
# usage: python3 tools/build.py
import html, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src" / "index.html").read_text(encoding="utf-8")
schools = json.loads((root / "schools.json").read_text(encoding="utf-8"))
cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
assert "__SCHOOLS__" in tpl and "__HUB_CONFIG__" in tpl and "<!--GOATCOUNTER-->" in tpl
blob = lambda v: json.dumps(v, ensure_ascii=False).replace("</", "<\\/")
gc = f'<script data-goatcounter="{html.escape(cfg["goatcounter"], quote=True)}" async src="https://gc.zgo.at/count.js"></script>' if cfg.get("goatcounter") else ""
pub = {k: cfg[k] for k in ("supabaseUrl", "supabaseKey") if cfg.get(k)}
out = tpl.replace("__SCHOOLS__", blob(schools)).replace("__HUB_CONFIG__", blob(pub)).replace("<!--GOATCOUNTER-->", gc)
(root / "site" / "index.html").write_text(out, encoding="utf-8")
print("site/index.html", len(out.encode()) // 1024, "KB,", len(schools), "schools")
