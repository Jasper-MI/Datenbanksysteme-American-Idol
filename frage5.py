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
#Frage 5
sql_query5 = """
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

# plot
cursor.execute(sql_query5)

result = cursor.fetchall()
for row in result:
    print(row)

kategorie, werte = zip(*result)

#plt.figure(figsize=(10, 6))
#plt.bar(kategorie, werte, color='skyblue')
#plt.xlabel('Geschlecht')
#plt.ylabel('Anzahl der Suchanfragen')
plt.title('Geschelchterverteilung')
#plt.show()

werte = [row[1] for row in result]
total = sum(werte)
plt.pie(werte, labels=kategorie, autopct=lambda p: '{:.0f}'.format(p * total / 100))
plt.show()


cursor.close()
connection.close()