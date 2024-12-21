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

# sql_queries

#Frage 1
sql_query1_2 = """
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

cursor.execute(sql_query1_2)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)


plt.bar(kategorie, werte, color='skyblue')
plt.xlabel('Tag')
plt.ylabel('Anzahl Suchanfragen')
plt.title('Suchanfragen nach Datum')
plt.show()

cursor.close()
connection.close()