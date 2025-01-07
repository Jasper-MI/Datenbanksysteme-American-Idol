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

#Frage 1_1: Suchanfragen nach Uhrzeit

sql_query = """
SELECT 
    EXTRACT(HOUR FROM "Uhrzeit") AS hour_of_day, 
    COUNT(*) AS entry_count
FROM 
    suchanfragen
WHERE 
    suchanfragen."Inhalt" ILIKE '%american idol%'
GROUP BY 
    EXTRACT(HOUR FROM "Uhrzeit")
ORDER BY 
    entry_count DESC
LIMIT 100;
"""

#Query ausführen
cur.execute(sql_query)

#Ergebnisse speichern
result = cur.fetchall()
#print(result)

#2 listen erstellen, liste 1: Uhrzeiten, liste 2: anzahl suchanfragen
uhrzeit, suchanfragen = zip(*result)
#print(uhrzeit)
#print(suchanfragen)

#Diagramme erstellen
plt.figure(facecolor='#f4f2f2')
plt.bar(uhrzeit, suchanfragen, color="#ff6b4d")
plt.xlabel('Uhrzeit')
plt.ylabel('Anzahl Suchanfragen')
plt.title('Suchanfragen nach Uhrzeiten')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()
