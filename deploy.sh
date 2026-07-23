#!/usr/bin/env bash
# Перший запуск. Використання: ./deploy.sh ТВІЙ_GITHUB_НІК
set -e
NICK="$1"
if [ -z "$NICK" ]; then echo "Вкажи GitHub-нік: ./deploy.sh artemhul"; exit 1; fi

git init -q 2>/dev/null || true
git add .
git commit -qm "El Clásico NFC Menu" || echo "Немає нових змін"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$NICK/elclasico-nfc-menu.git"
git push -u origin main

echo ""
echo "Готово. Лишилось увімкнути Pages:"
echo "  https://github.com/$NICK/elclasico-nfc-menu/settings/pages"
echo "  Source -> GitHub Actions -> Save"
echo ""
echo "Через хвилину сайт буде тут:"
echo "  https://$NICK.github.io/elclasico-nfc-menu/"
echo "  https://$NICK.github.io/elclasico-nfc-menu/qr.html"
