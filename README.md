# Omsa

För att starta flask:

Helst någon med Mac som kör kod.

WINDOWS
1. set FLASK_APP=main.py
2. $env:FLASK_APP = "main.py"
3. flask run

Installera Flask på MAC:
1. Högerklicka på mappen Omsa med den nedladdade filen
2. Klicka på ny terminal i mapp
3. Skriv i terminalen: python3 -m venv venv
4. . venv/bin/activate
5. pip install Flask
6. pip install psycopg2-binary
7. pip install --upgrade

För att start sidan på MAC
1. set FLASK_APP=main.py
2. export FLASK_APP=main
3. flask run