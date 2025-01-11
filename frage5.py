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

#Frage 5: Zusammenhang Suchanfragen mit Geschlecht der Person

sql_query = """
SELECT 
    besetzung."Geschlecht", 
    COUNT (*) AS anzahl_suchen
FROM 
    besetzung
JOIN
    suchanfragen
ON
    suchanfragen."Inhalt" = LOWER(besetzung."Name")
GROUP BY
    besetzung."Geschlecht";
"""

#Query ausführen
cur.execute(sql_query)

#Ergebnisse speichern
result = cur.fetchall()
#print(result)

#2 listen erstellen, liste 1: geschlecht, liste 2: anzahl suchanfragen
geschlecht, suchanfragen = zip(*result)
#print(geschlecht)
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
plt.pie(suchanfragen, labels=geschlecht, autopct=beschriftung)
plt.title('Suchanfragen nach Geschlecht der Besetzung')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()
