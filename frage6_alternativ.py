import psycopg2
import matplotlib.pyplot as plt
import numpy as np


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

cursor = conn.cursor()


# SQL-Abfrage
sql_query = """
SELECT
    CASE
        WHEN suchanfragen."Inhalt" ILIKE '%Black Horse and the Cherry Tree%' THEN 'Black Horse and the Cherry Tree'
        WHEN suchanfragen."Inhalt" ILIKE '%Song 2%' THEN 'Song 2'
        WHEN suchanfragen."Inhalt" ILIKE '%Song 3%' THEN 'Song 3'
    END AS song,
    SUM(CASE WHEN "Uhrzeit" < '2006-05-24' THEN 1 ELSE 0 END) AS vorher,
    SUM(CASE WHEN "Uhrzeit" >= '2006-05-24' THEN 1 ELSE 0 END) AS nachher
FROM 
    suchanfragen
WHERE
    suchanfragen."Inhalt" ILIKE '%Black Horse and the Cherry Tree%'
    OR suchanfragen."Inhalt" ILIKE '%Song 2%'
    OR suchanfragen."Inhalt" ILIKE '%Song 3%'
GROUP BY 
    song;
"""

# SQL-Abfrage ausführen
cursor = conn.cursor()
cursor.execute(sql_query)
result = cursor.fetchall()
conn.close()

# Ergebnisse überprüfen
print(result)  # Ausgabe in der Konsole: Liste von Tupeln [(song, vorher, nachher), ...]

# Daten für das Diagramm vorbereiten
songs = [row[0] for row in result]  # Songnamen
vorher = [row[1] for row in result]  # Werte für 'vorher'
nachher = [row[2] for row in result]  # Werte für 'nachher'

# X-Positionen für gruppierte Balken
x = np.arange(len(songs))  # Anzahl der Songs
width = 0.35  # Breite der Balken

# Balkendiagramm erstellen
fig, ax = plt.subplots(figsize=(10, 6))

# "Vorher"-Balken
bars1 = ax.bar(x - width/2, vorher, width, label='Vorher', color='skyblue')

# "Nachher"-Balken
bars2 = ax.bar(x + width/2, nachher, width, label='Nachher', color='orange')

# Titel und Labels
ax.set_xlabel('Songs', fontsize=12)
ax.set_ylabel('Anzahl der Suchanfragen', fontsize=12)
ax.set_title('Suchanfragen vor und nach dem 24. Mai 2006', fontsize=14, weight='bold')
ax.set_xticks(x)
ax.set_xticklabels(songs, rotation=45, ha='right')
ax.legend()

# Werte über die Balken schreiben
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 Punkte vertikal verschoben
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(bars1)
add_labels(bars2)

# Layout anpassen und Diagramm anzeigen
plt.tight_layout()
plt.show()

#Resourcen wieder schließen wenn fertig
cursor.close()
conn.close()