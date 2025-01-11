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

#Frage 9: Suche nach Skanale in der Show

sql_query = """
SELECT 
    CASE
        WHEN "Inhalt" ILIKE '%scandal%' THEN 'scandal'
        WHEN "Inhalt" ILIKE '%controversy%' THEN 'controversy'
    END AS kategorie,
    COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%american idol%' AND
    ("Inhalt" ILIKE '%scandal%'
    OR "Inhalt" ILIKE '%controversy%')
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
skandal, suchanfragen = zip(*result)
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
plt.pie(suchanfragen, labels=skandal, autopct=beschriftung)
plt.title('Wurde nach Skandalen in Bezug auf American Idol gesucht?')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()
