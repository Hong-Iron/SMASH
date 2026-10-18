# Builds site/index.html from src/index.html, schools.json and config.json.
# The school cards are also written into the HTML (not only built by JavaScript) so search crawlers see every game link.
# usage: python3 tools/build.py
import html, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src" / "index.html").read_text(encoding="utf-8")
schools = json.loads((root / "schools.json").read_text(encoding="utf-8"))
cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
for k in ("__SCHOOLS__", "__HUB_CONFIG__", "<!--GOATCOUNTER-->", "<!--JSONLD-->", "__CARDS__", "__COUNT__"):
    assert k in tpl, k
e = lambda v: html.escape(str(v), quote=True)
blob = lambda v: json.dumps(v, ensure_ascii=False).replace("</", "<\\/")
gc = f'<script data-goatcounter="{e(cfg["goatcounter"])}" async src="https://gc.zgo.at/count.js"></script>' if cfg.get("goatcounter") else ""
pub = {k: cfg[k] for k in ("supabaseUrl", "supabaseKey") if cfg.get(k)}
by_name = sorted(schools, key=lambda s: s["name"])  # same order as the page's default "이름순"; the script re-sorts with Korean collation
cards = "".join(
    f'<a class="card" href="{e(s["url"])}"><img src="{e(s["url"])}og.png" alt="{e(s["campus"])}가 부서지는 게임 화면" loading="lazy" width="1200" height="630">'
    f'<div class="body"><span class="code">SMASH {e(s["code"])}</span><span class="name">{e(s["campus"])}</span>'
    f'<span class="region">{e(s.get("region", ""))}</span><span class="meta">건물 {e(s["buildings"])}동</span><span class="go">부수러 가기 →</span></div></a>'
    for s in by_name)
ld = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "name": "SMASH 대학교", "alternateName": "우리 학교 부수기 게임", "url": "https://hong-iron.github.io/SMASH/", "inLanguage": "ko"},
        {"@type": "ItemList", "name": "SMASH 대학교 캠퍼스 목록", "numberOfItems": len(schools),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": s["url"], "name": f'{s["campus"]} 부수기 게임'} for i, s in enumerate(by_name)]},
        # breadcrumb: Google shows "Hong-Iron › SMASH 대학교" in place of the bare address
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Hong-Iron", "item": "https://hong-iron.github.io/"},
            {"@type": "ListItem", "position": 2, "name": "SMASH 대학교", "item": "https://hong-iron.github.io/SMASH/"}]},
    ],
}
out = (tpl.replace("__SCHOOLS__", blob(schools)).replace("__HUB_CONFIG__", blob(pub)).replace("<!--GOATCOUNTER-->", gc)
       .replace("<!--JSONLD-->", '<script type="application/ld+json">' + blob(ld) + "</script>")
       .replace("__CARDS__", cards).replace("__COUNT__", str(len(schools))))
(root / "site" / "index.html").write_text(out, encoding="utf-8")
print("site/index.html", len(out.encode()) // 1024, "KB,", len(schools), "schools")
