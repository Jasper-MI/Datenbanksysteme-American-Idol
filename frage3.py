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


# sql_querie
# Frage 3
sql_query3 = """
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

# plot

cursor.execute(sql_query3)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)

plt.pie(werte, labels=kategorie)
plt.title('Suchanfragen pro Uhrzeit')
plt.show()


cursor.close()
connection.close()