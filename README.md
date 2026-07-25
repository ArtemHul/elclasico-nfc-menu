# El Clásico · NFC Menu

Онлайн-меню для **El Clásico Football Bar** — C. de la Virgen del Socorro, 39, 03002 Alicante.
Одна сторінка, вісім мов, фільтр алергенів, QR і NFC. Хостинг — Cloudflare Pages, безкоштовно.

Меню оцифроване з фото двох карт (крейдяної дошки + друкованого буклета).
Дублікати страв усунені, все зведене в одну карту зі 104 позиціями у 14 розділах.

---

## Де живе сайт

**https://elclasico-nfc-menu.pages.dev**

Деплой автоматичний: кожен push у `main` — і Cloudflare сам пересобирає та публікує
сайт за 1–3 хвилини. Робити нічого не треба.

Налаштування збірки в панелі Cloudflare (Workers & Pages → проєкт → Settings → Build):

| Поле | Значення |
|---|---|
| Build command | `python3 scripts/build.py` |
| Build output directory | `docs` |
| Framework preset | None |

Версію Python задає файл `.python-version` у корені.

Той самий сайт паралельно лишається на GitHub Pages як запасний:
`https://artemhul.github.io/elclasico-nfc-menu/`

**QR для столів**

Відкрий **https://elclasico-nfc-menu.pages.dev/qr** — адреса меню підставиться сама,
лишиться вказати кількість столів і надрукувати.

Зверни увагу: саме `/qr`, без `.html`. Cloudflare зрізає розширення в адресах.

---

## Структура

```
data/menu.json          дані меню — тут міняються страви й ціни
template.html           шаблон (верстка, стилі, палітра, шапка)
docs/index.html         зібраний сайт — генерується автоматично
docs/qr.html            генератор QR для друку
scripts/build.py        menu.json -> docs/index.html
scripts/build_data.py   вихідний генератор menu.json (довідково)
.github/workflows/      автозбірка при кожному push
```

**Не редагуй `docs/index.html` вручну** — його перезапише збірка.
Дані міняй у `data/menu.json`, зовнішній вигляд — у `template.html`.

---

## Як міняти меню

Відкрий `data/menu.json`, знайди страву, зміни `p` (ціну) або текст, зроби commit —
сайт оновиться сам за хвилину. Кожна страва має формат:

```json
{
  "p": "6,80",
  "alg": ["gluten","lacteos"],
  "n": { "es": "...", "en": "...", "de": "...", "fr": "...", "nl": "...", "it": "...", "uk": "...", "ru": "..." },
  "d": { "es": "...", "en": "...", "de": "...", "fr": "...", "nl": "...", "it": "...", "uk": "...", "ru": "..." },
  "pop": true
}
```

`pop: true` додає позначку «Популярне». Прибери рядок, якщо не треба.

### Алергени

Коди в масиві `alg` (офіційні 14 за Reglamento UE 1169/2011):

`gluten` `crustaceos` `huevo` `pescado` `cacahuetes` `soja` `lacteos`
`frutos` `apio` `mostaza` `sesamo` `sulfitos` `altramuces` `moluscos`

Збірка перевіряє коди й попереджає про незнайомі та про пропущені переклади.

---

## Локальна робота

```bash
python3 scripts/build.py
python3 -m http.server -d docs 8000   # відкрий http://localhost:8000
```

---

## Що в меню

14 розділів: Tapas · Especiales de pizarra · Ensaladas · Tostas · Pasta · Tablas ·
Bocadillos · Hamburguesas · Crepes · Postres y helados · Batidos · Bebidas · Cócteles · Cafés.

- **8 мов** з автовизначенням за мовою телефона (es/en/de/fr/nl/it/uk/ru)
- **Фільтр алергенів** — 7 типів, включно з сульфітами (вино, сангрія)
- **Номер столу** з мітки: `?t=7`
- **Без залежностей** — один HTML, ~97 КБ

---

## Перед запуском звірити з власником

- **Телефон, Instagram** — зараз заглушки в `template.html`
- **Алергени** проставлені за складом страв — це припущення, звір із кухнею
- **Крейдяна дошка**: назви Marinera / Matrimonio нерозбірливі, переклав як анчоусні тапас
- **Години роботи** — заглушка «дивись розклад матчів»

Юридично: паперове меню тримати за запитом гостя; алергени — відповідальність закладу.

---

## NFC

Мітки NTAG213. Пиши свій домен із редиректом, а не пряме посилання на Pages —
інакше при переїзді доведеться перепрошивати всі мітки. Блокуй від перезапису (lock).
На металі потрібні on-metal мітки або корпус із PETG.
