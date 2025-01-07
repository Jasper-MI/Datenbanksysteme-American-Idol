import psycopg2
import matplotlib.pyplot as plt

#Datenbankattribute
host = "localhost"
port = 5432
name = "aol_data"
user = "postgres"
pwd = "password"

#connection zur DB herstellen
try:
    conn = psycopg2.connect(
        host = host,
        port = port,
        database = name,
        user = user,
        password = pwd
    )
    print("Verbindung erfolgreich :)")
except Exception as e:
    print("Fehler beim verbinden: ", e)

#cursor erstellen um sql-statements auszuführen
cur = conn.cursor()

#Frage 7: Fragen zu technischen Kontext

sql_query = """
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

#Query ausführen
cur.execute(sql_query)

#Ergebnisse speichern
result = cur.fetchall()
#print(result)

#2 listen erstellen, liste 1: fragewort, liste 2: anzahl suchanfragen
frage, suchanfragen = zip(*result)
#print(frage)
#print(suchanfragen)

#Diagramme erstellen
plt.pie(suchanfragen, labels=frage)
plt.title('Technische Fragen zu American Idol')
plt.show()

#Resourcen wieder schließen wenn fertig
cur.close()
conn.close()