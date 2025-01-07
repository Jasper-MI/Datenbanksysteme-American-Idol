import psycopg2
import matplotlib.pyplot as plt

#Datenbankattribute
host = "localhost"
port = 5432
name = "******"
user = "postgres"
pwd = "********"

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

#Frage 10: Suche nach Spoilern

sql_query = """
SELECT 
    CASE
        WHEN "Inhalt" ILIKE '%spoiler%' THEN 'spoiler'
        WHEN "Inhalt" ILIKE '%winner%' OR "Inhalt" ILIKE '%won%' THEN 'winner/won'

    END AS kategorie,
    COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%american idol%' AND
    ("Inhalt" ILIKE '%spoiler%'
    OR (
        "Inhalt" ILIKE '%winner%'
        OR "Inhalt" ILIKE '%won%'
        )
    )
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

#2 listen erstellen, liste 1: fragewort, liste 2: anzahl suchanfragen
spoiler, suchanfragen = zip(*result)
#print(skandal)
#print(suchanfragen)

#Gesamte Anzahl der Suchanfragen um es im Pie Diagramm darzustellen
total=sum(suchanfragen)

#pct kommt von 'autopct', funktion gibt die absoluten suchanfragen für die beschriftung zurück
def beschriftung(pct):
    absolut = int(round(pct * total / 100))
    #rückgabe absolutwerte als string
    return str(absolut)

#Diagramme erstellen
plt.figure(facecolor='#f4f2f2')
plt.pie(suchanfragen, labels=spoiler, autopct=beschriftung)
plt.title('Wie wurde nach Spoilern zu American Idol gesucht?')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()