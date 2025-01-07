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

#Frage 3: User die immer wieder gesucht haben

sql_query = """
SELECT 
    "BenutzerID", COUNT (*) AS count_anonid
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%american idol%'
GROUP BY 
    "BenutzerID"
ORDER BY 
    count_anonid DESC
    LIMIT 25;
"""

#Query ausführen
cur.execute(sql_query)

#Ergebnisse speichern
result = cur.fetchall()
#print(result)

#2 listen erstellen, liste 1: User, liste 2: anzahl suchanfragen
user, suchanfragen = zip(*result)
#print(user)
#print(suchanfragen)

#Diagramme erstellen
plt.figure(facecolor='#f4f2f2')
plt.pie(suchanfragen, labels=user)
plt.title('Suchanfragen nach User')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()