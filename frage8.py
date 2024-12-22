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
    "Inhalt", COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%americian idol%'
    OR "Inhalt" ILIKE '%amerian idol%'
    OR "Inhalt" ILIKE '%american idole%'
    OR "Inhalt" ILIKE '%amerian idle%'
    OR "Inhalt" ILIKE '%amerian idool%'
    OR "Inhalt" ILIKE '%aqmericaqn idol%'
    OR ("Inhalt" ILIKE '%a%m%e%r%i%a%n %i%d%o%l%' AND "Inhalt" NOT ILIKE 'american idol%')
GROUP BY 
    "Inhalt"
ORDER BY 
    anzahl DESC;
"""

cursor.execute(sql_query8)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)


plt.pie(kategorie, werte, color='skyblue')
#plt.xlabel('Uhrzeit')
#plt.ylabel('Anzahl Suchanfragen')
plt.title('Häufige Rechtschreibfehler')
plt.show()

cursor.close()
connection.close()