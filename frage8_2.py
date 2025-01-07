import psycopg2
import matplotlib.pyplot as plt

#Datenbankattribute
host = "localhost"
port = 5432
name = "aol_data"
user = "postgres"
pwd = "password"

#connection zur DB herstellen
try:
    conn = psycopg2.connect(
        host = host,
        port = port,
        database = name,
        user = user,
        password = pwd
    )
    print("Verbindung erfolgreich :)")
except Exception as e:
    print("Fehler beim verbinden: ", e)

#cursor erstellen um sql-statements auszuführen
cur = conn.cursor()

#Frage 8: Häufige Rechtschreibfehler

sql_query = """
SELECT 
    CASE
        WHEN "Inhalt" ILIKE '%americian idol%' THEN 'americian idol'
        WHEN "Inhalt" ILIKE '%amerian idol%' THEN 'amerian idol'
        WHEN "Inhalt" ILIKE '%american idole%' THEN 'american idole'
        WHEN "Inhalt" ILIKE '%amerian idle%' THEN 'amerian idle'
        WHEN "Inhalt" ILIKE '%amerian idool%' THEN 'amerian idool'
        WHEN "Inhalt" ILIKE '%aqmericaqn idol%' THEN 'aqmericaqn idol'
        ELSE 'Unbekannt'
    END AS kategorie,
    COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%americian idol%'
    OR "Inhalt" ILIKE '%amerian idol%'
    OR "Inhalt" ILIKE '%american idole%'
    OR "Inhalt" ILIKE '%amerian idle%'
    OR "Inhalt" ILIKE '%amerian idool%'
    OR "Inhalt" ILIKE '%aqmericaqn idol%'
GROUP BY 
    kategorie
ORDER BY 
    anzahl DESC;
"""

#Query ausführen
cur.execute(sql_query)

#Ergebnisse speichern
result = cur.fetchall()
#print(result)

#2 listen erstellen, liste 1: schreibfehler, liste 2: anzahl
schreibfehler, anzahl = zip(*result)
#print(schreibfehler)
#print(anzahl)

#Diagramme erstellen
plt.pie(anzahl, labels=schreibfehler)
plt.title('Suchanfragen zu American Idol mit Rechtschreibfehler')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()