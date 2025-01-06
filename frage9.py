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

#Frage 9
sql_query9 = """
SELECT 
    CASE
        WHEN "Inhalt" ILIKE '%scandal%' THEN 'scandal'
        WHEN "Inhalt" ILIKE '%controversy%' THEN 'controversy'
    END AS kategorie,
    COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%american idol%' AND
    ("Inhalt" ILIKE '%scandal%'
    OR "Inhalt" ILIKE '%controversy%')
GROUP BY 
    kategorie
ORDER BY 
    anzahl DESC;
"""

cursor.execute(sql_query9)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)


plt.pie(werte, labels=kategorie)
#plt.xlabel('Uhrzeit')
#plt.ylabel('Anzahl Suchanfragen')
plt.title('Suche nach Skandale')
plt.show()

cursor.close()
connection.close()