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

#Frage 8
sql_query8 = """
SELECT 
    CASE
        WHEN "Inhalt" ILIKE '%americian idol%' THEN 'americian idol'
        WHEN "Inhalt" ILIKE '%amerian idol%' THEN 'amerian idol'
        WHEN "Inhalt" ILIKE '%american idole%' THEN 'american idole'
        WHEN "Inhalt" ILIKE '%amerian idle%' THEN 'amerian idle'
        WHEN "Inhalt" ILIKE '%amerian idool%' THEN 'amerian idool'
        WHEN "Inhalt" ILIKE '%aqmericaqn idol%' THEN 'aqmericaqn idol'
        ELSE 'Unbekannt'
    END AS kategorie,
    COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%americian idol%'
    OR "Inhalt" ILIKE '%amerian idol%'
    OR "Inhalt" ILIKE '%american idole%'
    OR "Inhalt" ILIKE '%amerian idle%'
    OR "Inhalt" ILIKE '%amerian idool%'
    OR "Inhalt" ILIKE '%aqmericaqn idol%'
GROUP BY 
    kategorie
ORDER BY 
    anzahl DESC;
"""

cursor.execute(sql_query8)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)


plt.pie(werte, labels=kategorie)
#plt.xlabel('Uhrzeit')
#plt.ylabel('Anzahl Suchanfragen')
plt.title('Häufige Rechtschreibfehler')
plt.show()

cursor.close()
connection.close()