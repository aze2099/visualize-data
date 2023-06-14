# Visualize-data (JSON 2 Excel) för Webperf Core
Gör en överskådlig excelfil utifrån en JSON-körning i webperf-core. Kolumner för "URL - testresultat1 - testkommentarer1 - testresultat2 - testkommentar2 etc". Städar även bort underbetyg som fått resultat 5 så man bara får de punkter man behöver fokusera på. Huvudbetygets femmor är kvar. Sortera respektive kolumn i ökande ordning för att få sämst resultat överst.

# Användning
I terminalen; kör filen med "Python import-data.py [sökväg\]filnamn.json". Resultatet blir en excelfil i körningsmappen vid namn "[datum]_test_results.xlsx".

# Installationskrav
- Pandas: Ett dataanalysbibliotek i Python. Det kan installeras med pip, Pythons pakethanterare, genom att skriva "pip install pandas" i terminalen.
- openpyxl: En Python-bibliotek för att läsa/skriva Excel 2010 xlsx/xlsm/xltx/xltm filer. Installera med "pip install openpyxl".
