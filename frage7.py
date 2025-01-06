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
        WHEN "Inhalt" ILIKE '%phone%' THEN 'phone'
        WHEN "Inhalt" ILIKE '%phone%' THEN 'vote'
        WHEN "Inhalt" ILIKE '%phone%' THEN 'online'
        WHEN "Inhalt" ILIKE '%phone%' THEN 'how'
        WHEN "Inhalt" ILIKE '%where%' THEN 'where'
        WHEN "Inhalt" ILIKE '%voting%' THEN 'voting'
        WHEN "Inhalt" ILIKE '%internet%' THEN 'internet'
        WHEN "Inhalt" ILIKE '%count%' THEN 'count'
        WHEN "Inhalt" ILIKE '%rule%' THEN 'rule'
        WHEN "Inhalt" ILIKE '%registration%' THEN 'registration'
        WHEN "Inhalt" ILIKE '%number%' THEN 'number'
        WHEN "Inhalt" ILIKE '%hotlines%' THEN 'hotlines'
        ELSE 'Unbekannt'
    END AS kategorie,
    COUNT(*) AS anzahl
FROM 
    suchanfragen
WHERE 
    "Inhalt" ILIKE '%american idol%'
    AND ( "Inhalt" ILIKE '%phone%'
    OR "Inhalt" ILIKE '%phone%'
    OR "Inhalt" ILIKE '%phone%'
    OR "Inhalt" ILIKE '%phone%'
    OR "Inhalt" ILIKE '%where%'
    OR "Inhalt" ILIKE '%voting%'
    OR "Inhalt" ILIKE '%internet%'
    OR "Inhalt" ILIKE '%count%'
    OR "Inhalt" ILIKE '%rule%'
    OR "Inhalt" ILIKE '%registration%'
    OR "Inhalt" ILIKE '%number%'
    OR "Inhalt" ILIKE '%hotlines%'
    )
    
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