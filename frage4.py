import psycopg2
import matplotlib.pyplot as plt

DB_HOST = "db_host"
DB_PORT = 1234
DB_NAME = "db_name"
DB_USER = "db_user"
DB_PASS = "db_pass"

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
#Frage 4
sql_query4 = """
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

# plot

cursor.execute(sql_query4)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)

plt.bar(kategorie, werte, color='skyblue')
plt.ylabel('Anzahl der Suchanfragen')
plt.title('Vergleich mit "American Idol"')
plt.show()


cursor.close()
connection.close()