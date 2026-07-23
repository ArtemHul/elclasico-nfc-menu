#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Вставляє data/menu.json у template.html і пише docs/index.html.

Палітра, шапка, шрифти й тексти вже вшиті в template.html.
Цей скрипт міняє лише блок `const DATA = {...}` — тобто самі страви.

Використання:
    python3 scripts/build.py                # data/menu.json -> docs/index.html
    python3 scripts/build.py data/menu.json template.html docs/index.html
"""
import json, re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src   = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "data" / "menu.json"
tmpl  = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else root / "template.html"
out   = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else root / "docs" / "index.html"

data = json.loads(src.read_text(encoding="utf-8"))
html = tmpl.read_text(encoding="utf-8")

# --- валідація алергенів ---
OFFICIAL = {"gluten","crustaceos","huevo","pescado","cacahuetes","soja","lacteos",
            "frutos","apio","mostaza","sesamo","sulfitos","altramuces","moluscos"}
warn = 0
seen_names = {}
for s in data["sections"]:
    for i in s["items"]:
        for a in i["alg"]:
            if a not in OFFICIAL:
                print(f"⚠ невідомий алерген '{a}' у страві {i['n'].get('es','?')}"); warn += 1
        # ціна
        if not re.match(r"^\d+([.,]\d{1,2})?$", str(i["p"])):
            print(f"⚠ дивна ціна '{i['p']}' у {i['n'].get('es','?')}"); warn += 1
        # переклади
        for field in ("n","d"):
            es = i[field].get("es","")
            for lng in ("en","de","fr","nl","uk"):
                if es and not i[field].get(lng):
                    print(f"⚠ пропущено переклад {field}.{lng}: {es}"); warn += 1
        # дублікати назв (es)
        nm = i["n"].get("es","").lower()
        seen_names[nm] = seen_names.get(nm, 0) + 1

for nm, c in seen_names.items():
    if c > 1:
        print(f"⚠ можливий дубль страви: '{nm}' зустрічається {c}×")

# --- підміна блоку DATA ---
new_block = "const DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";"
html2, n = re.subn(r"const DATA = \{.*?\n\};", new_block, html, count=1, flags=re.S)
if n != 1:
    print("✗ не знайдено блок `const DATA = {...}` у template.html"); sys.exit(1)

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html2, encoding="utf-8")

secs = len(data["sections"])
items = sum(len(s["items"]) for s in data["sections"])
print(f"✓ Готово: {out}")
print(f"  Розділів: {secs} · Позицій: {items} · Попереджень: {warn}")
