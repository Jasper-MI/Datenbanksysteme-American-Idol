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

#Frage 4: Vergleiche mit anderen Shows

sql_query = """
SELECT 
    shows."Titel", 
    COUNT(suchanfragen."SearchID") AS anzahl_suchen
FROM
    shows
LEFT JOIN
    shows_suchanfragen
ON
    shows."ShowID" = shows_suchanfragen."ShowID"
LEFT JOIN
    suchanfragen
ON
    suchanfragen."SearchID" = shows_suchanfragen."SearchID"
    AND suchanfragen."Inhalt" ILIKE '%american idol%'
WHERE
	shows."Titel" != 'American Idol'
GROUP BY
    shows."Titel";
"""

#Query ausführen
cur.execute(sql_query)

#Ergebnisse speichern
result = cur.fetchall()
#print(result)

#2 listen erstellen, liste 1: User, liste 2: anzahl suchanfragen
show, suchanfragen = zip(*result)
#print(show)
#print(suchanfragen)

#Diagramme erstellen
plt.figure(facecolor='#f4f2f2')
plt.bar(show, suchanfragen, color="#ff6b4d")
plt.xlabel('Shows')
plt.ylabel('suchanfragen')
plt.title('Suchanfragen nach User')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()