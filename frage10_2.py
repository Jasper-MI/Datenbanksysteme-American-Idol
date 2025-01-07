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

#Frage 10: Suche nach Spoilern

sql_query =  """
SELECT 
    DATE("Uhrzeit") AS hour_of_day, 
    COUNT(*) AS entry_count
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
    DATE("Uhrzeit")
ORDER BY 
    entry_count DESC;
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

#Diagramme erstellen
plt.figure(facecolor='#f4f2f2')
plt.bar(spoiler, suchanfragen, color='#ff6b4d')
plt.xlabel('Tag')
plt.ylabel('Anzahl Suchanfragen')
plt.title('Suchanfragen nach Spoilern')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()