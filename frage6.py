import psycopg2
import matplotlib.pyplot as plt

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "sql.datenbank"

try:
    connection = psycopg2.connect(
        host = DB_HOST,
        port = DB_PORT,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )
    print("Verbindung erfolgreich :)")
except Exception as e:
    print("Fehler beim Verbinden: ", e)

cursor = connection.cursor()


# sql_query
#Frage 6
sql_query6 = """
SELECT 
    'Vorher' AS Zeitraum,
    COUNT (*) AS anzahl_suchanfragen
FROM 
    suchanfragen
WHERE
    "Inhalt" ILKIKE '%Black Horse and the Cherry Tree%'
    AND "Uhrzeit" < '2006-05-24'

UNION ALL

SELECT 
    'Nachher' AS Zeitraum,
    COUNT (*) AS anzahl_suchanfragen
FROM 
    suchanfragen
WHERE
    "Inhalt" ILKIKE '%Black Horse and the Cherry Tree%'
    AND "Uhrzeit" >= '2006-05-24';
"""


# plot

cursor.execute(sql_query6)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)

plt.figure(figsize=(10, 6))
plt.bar(kategorie, werte, color='skyblue')
plt.xlabel('Geschlecht')
plt.ylabel('Anzahl der Suchanfragen')
plt.title('Geschelchterverteilung')
plt.show()


cursor.close()
connection.close()