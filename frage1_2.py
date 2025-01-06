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

#Frage 1_2: Suchanfragen nach Tag

sql_query = """
SELECT 
    DATE("Uhrzeit") AS hour_of_day, 
    COUNT(*) AS entry_count
FROM 
    suchanfragen
WHERE 
    suchanfragen."Inhalt" ILIKE '%american idol%'
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

#2 listen erstellen, liste 1: Tage, liste 2: anzahl suchanfragen
tag, suchanfragen = zip(*result)
#print(tag)
#print(suchanfragen)

#Diagramme erstellen
plt.bar(tag, suchanfragen, color="#ff6b4d")
plt.xlabel('Tag')
plt.ylabel('Anzahl Suchanfragen')
plt.title('Suchanfragen nach Tagen')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()