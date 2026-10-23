# Builds site/index.html from src/index.html, schools.json and config.json.
# The school cards are also written into the HTML (not only built by JavaScript) so search crawlers see every game link.
# usage: python3 tools/build.py
import html, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src" / "index.html").read_text(encoding="utf-8")
schools = json.loads((root / "schools.json").read_text(encoding="utf-8"))
cfg = json.loads((root / "config.json").read_text(encoding="utf-8"))
nf = root / "notices.json"   # 공지 카드: [{id, date, until, tag, title, body, url, image, cta}]
notices = json.loads(nf.read_text(encoding="utf-8")) if nf.exists() else []
for k in ("__NOTICES__", "__SCHOOLS__", "__HUB_CONFIG__", "<!--GOATCOUNTER-->", "<!--JSONLD-->", "__CARDS__", "__COUNT__", "__MAP__"):
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
def notice(n):
    m, d = (int(x) for x in n["date"].split("-")[1:])
    return (f'<a class="notice" href="{e(n["url"])}" data-id="{e(n["id"])}" data-until="{e(n.get("until", ""))}">'
            f'<img src="{e(n["image"])}" alt="{e(n["title"])} 화면" width="1200" height="630">'
            f'<div class="body"><span class="tag">{e(n.get("tag", "공지"))} · <time datetime="{e(n["date"])}">{m}월 {d}일</time></span>'
            f'<strong>{e(n["title"])}</strong><span class="text">{e(n["body"])}</span><span class="go">{e(n.get("cta", "보러 가기"))} →</span></div></a>')
notice_html = (f'<section class="notices" aria-labelledby="notice-title"><h2 class="sec-title" id="notice-title">공지</h2>'
               f'{"".join(notice(n) for n in notices)}</section>') if notices else ""
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
# 지도: 남한 시도 경계(KOSTAT 2013, 자유 이용 — github.com/southkorea/southkorea-maps)를 SVG 경로로, 학교는 같은 투영의 좌표(mx, my)로
import math
LON0, LAT1, K = 124.5, 38.75, 100.0
KX = K * math.cos(math.radians(36.2))
proj = lambda lon, lat: (round((lon - LON0) * KX, 1), round((LAT1 - lat) * K, 1))
prov = json.loads((root / "tools" / "korea_provinces.json").read_text(encoding="utf-8"))
INSET_DX, INSET_DY = -1.3, 0.95   # 울릉도·독도(동경 130.5° 동쪽)는 지도 오른쪽 위 바다의 상자 안으로 옮겨 그린다
def ring_d(ring):
    pts, last = [], None
    shift = INSET_DX if min(lon for lon, _ in ring) > 130.5 else 0
    for lon, lat in ring:
        q = proj(lon + shift, lat + (INSET_DY if shift else 0))
        if q != last: pts.append(q); last = q
    return "M" + "L".join(f"{x:g},{y:g}" for x, y in pts) + "Z" if len(pts) > 2 else ""
paths = []
for f in prov["features"]:
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    paths.append(f'<path class="prov" d="{"".join(ring_d(r) for poly in polys for r in poly)}"><title>{e(f["properties"]["name"])}</title></path>')
dx, dy = proj(131.8667 + INSET_DX, 37.2417 + INSET_DY)
ix0, iy0 = proj(130.65 + INSET_DX, 37.7 + INSET_DY); ix1, iy1 = proj(132.0 + INSET_DX, 37.12 + INSET_DY)
paths.append(f'<g class="inset"><rect x="{ix0}" y="{iy0}" width="{round(ix1-ix0,1)}" height="{round(iy1-iy0,1)}" rx="3"/></g>')
ux, uy = proj(130.87 + INSET_DX, 37.5 + INSET_DY)
paths.append(f'<g class="dokdo"><circle cx="{dx}" cy="{dy}" r="1.6"/><circle cx="{dx+2.4}" cy="{dy+0.6}" r="1.2"/></g>'
             f'<text class="isl" x="{dx+1}" y="{dy-6}" text-anchor="middle">독도</text><text class="isl" x="{ux}" y="{uy-9}" text-anchor="middle">울릉도</text>')
W, Hh = proj(130.78, 33.0)
map_svg = f'<svg class="kmap" id="kmap" viewBox="0 0 {W} {Hh}" data-w="{W}" data-h="{Hh}" role="img" aria-label="남한 지도와 학교 위치"><rect class="sea" x="-2000" y="-2000" width="5000" height="5000"/><g id="kmap-land">{"".join(paths)}</g><g id="kmap-dots"></g></svg>'
for s in schools:
    s["mx"], s["my"] = proj(s["lon"], s["lat"])
out = (tpl.replace("__SCHOOLS__", blob(schools)).replace("__HUB_CONFIG__", blob(pub)).replace("<!--GOATCOUNTER-->", gc)
       .replace("<!--JSONLD-->", '<script type="application/ld+json">' + blob(ld) + "</script>")
       .replace("__NOTICES__", notice_html).replace("__MAP__", map_svg).replace("__CARDS__", cards).replace("__COUNT__", str(len(schools))))
(root / "site" / "index.html").write_text(out, encoding="utf-8")
print("site/index.html", len(out.encode()) // 1024, "KB,", len(schools), "schools")
