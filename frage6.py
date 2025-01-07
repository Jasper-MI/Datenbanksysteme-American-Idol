import psycopg2
import matplotlib.pyplot as plt

host = "localhost"
port = 5432
name = "aol_data"
user = "postgres"
pwd = "password"

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
songtitel = "Levon"
sql_query6 = f"""
SELECT 
    'Vorher' AS Zeitraum,
    COUNT (*) AS anzahl_suchanfragen
FROM 
    suchanfragen
WHERE
    -- Hier Songtitel austauschen
    "Inhalt" ILIKE '%{songtitel}%'
    AND "Uhrzeit" < '2006-05-24'

UNION ALL

SELECT 
    'Nachher' AS Zeitraum,
    COUNT (*) AS anzahl_suchanfragen
FROM 
    suchanfragen
WHERE
    -- Hier Songtitel austauschen
    "Inhalt" ILIKE '%{songtitel}%'
    AND "Uhrzeit" >= '2006-05-24';
"""


# plot

cursor.execute(sql_query6)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)


plt.figure(figsize=(10, 6), facecolor='#f4f2f2')
plt.bar(kategorie, werte, color='#ff6b4d')
plt.xlabel(songtitel)
plt.ylabel('Anzahl der Suchanfragen')
plt.title('Vergleich der Suchanfragen vor und nach dem Auftritt von Songs')
plt.show()


cursor.close()
connection.close()