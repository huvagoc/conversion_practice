markdown_content = """# Átváltás-kvíz 🎓

Egy egyszerű, böngészőben futó kvíz alkalmazás **5. osztályos mértékegység-átváltáshoz**, a magyar tantervnek megfelelően. Letöltés és telepítés nélkül használható – egyetlen `.html` fájl, amely bármilyen eszközön (telefon, tablet, PC) működik.

## Célja
Az 5. osztályos matematika anyagához igazodó, interaktív gyakorló eszköz. A tanuló saját tempójában, játékos formában ismételheti az anyagot – bárhol, akár internetkapcsolat nélkül is.

## Funkciók
- **5 kategória:** Hosszúság, Terület, Térfogat, Tömeg és Idő (a beállításokban kiválasztható, melyik legyen aktív).
- **Változatos feladatok:** Kétirányú (kicsi→nagy és nagy→kicsi) átváltások, felváltva. Minden 4. kérdésnél "dupla ugrással" (pl. mm → dm).
- **Magyar szabvány:** Tizedesvessző használata a megjelenítésben (bevitelnél a pont is érvényes), és vegyes időkijelzés (pl. 1,5 óra helyett „1 óra 30 perc").
- **Gördülékeny játék:** Helyes válasz esetén automatikus továbblépés (rövid visszajelzés után), a végén eredményképernyő érem-visszajelzéssel (🥇🥈🥉💪).
- **Mobilra optimalizált:** Okos elrendezés, amely alkalmazkodik a felugró virtuális billentyűzethez, beépített automatikus sötét móddal.

## Telepítés / Használat
Nyisd meg bármilyen böngészőben (Chrome, Safari, Firefox stb.).
*Megjegyzés: A futtatáshoz semmilyen szerver vagy állandó internetkapcsolat nem szükséges.*

## Technikai háttér
- Keretrendszer nélküli, tiszta **HTML/CSS/JS** megoldás, külső függőségek nélkül.
- A véletlenszám-generátor garantálja, hogy a **válasz minden esetben egész szám**, a forrásérték pedig legfeljebb 2 tizedesjegyű.
- A kód könnyen olvasható, az egységpárok és kategóriák a kódon belül egyszerűen bővíthetők.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("File generated successfully.")