import anvil.server
import sqlite3
import random
import string
from datetime import datetime


def get_connection():
    return sqlite3.connect('mittelalter.db')

@anvil.server.callable
def reset_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS Koenige;''')
    cursor.execute('''DROP TABLE IF EXISTS Burgen;''')
    cursor.execute('''DROP TABLE IF EXISTS Ritter;''')
    cursor.execute('''DROP TABLE IF EXISTS Doerfer;''')
    cursor.execute('''DROP TABLE IF EXISTS Schlachten;''')
    cursor.execute('''DROP TABLE IF EXISTS Ritter_Schlachten;''')
    cursor.execute('''DROP TABLE IF EXISTS Armeen;''')
    conn.commit()
    conn.close()

@anvil.server.callable
def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Koenige (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        thronbeginn DATE NOT NULL,
        thronende DATE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Burgen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ort TEXT NOT NULL,
        erbaut_im YEAR,
        koenig_id INTEGER,
        FOREIGN KEY (koenig_id) REFERENCES Koenige(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ritter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rang TEXT,
        geburtsjahr INTEGER,
        burg_id INTEGER,
        geheimes_passwort TEXT,  -- neues Feld für geheime Phrase
        FOREIGN KEY (burg_id) REFERENCES Burgen(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Doerfer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bewohnerzahl INTEGER,
        burg_id INTEGER,
        FOREIGN KEY (burg_id) REFERENCES Burgen(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schlachten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        datum DATE NOT NULL,
        burg_1_id INTEGER,
        burg_2_id INTEGER,
        sieger_burg_id INTEGER,
        FOREIGN KEY (burg_1_id) REFERENCES Burgen(id),
        FOREIGN KEY (burg_2_id) REFERENCES Burgen(id),
        FOREIGN KEY (sieger_burg_id) REFERENCES Burgen(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ritter_Schlachten (
        ritter_id INTEGER,
        schlacht_id INTEGER,
        rolle TEXT,
        PRIMARY KEY (ritter_id, schlacht_id),
        FOREIGN KEY (ritter_id) REFERENCES Ritter(id),
        FOREIGN KEY (schlacht_id) REFERENCES Schlachten(id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Armeen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ritter_id INTEGER,
        anzahl INTEGER,
        FOREIGN KEY (ritter_id) REFERENCES Ritter(id)
    );
    ''')

    conn.commit()
    conn.close()

# Hilfsfunktion für ein zufälliges Passwort (geheime Phrase)
def generate_secret_phrase(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@anvil.server.callable
def fill_database():
    conn = get_connection()
    cursor = conn.cursor()

    koenige_namen = ['Aldric', 'Berengar', 'Willelm', 'Thorin', 'Oswin', 'Eldric', 'Lothar', 'Georg', 'Erik', 'Sigurd']
    burgen_namen = ['Drachenstein', 'Eisenwall', 'Felsenburg', 'Goldberg', 'Eisenschmiede', 'Schattenburg', 'Burg der Ahnen', 'Sturmfels', 'Hohenstein', 'Weißhorn']
    burgen_orte = ['Nordreich', 'Südmark', 'Westland', 'Ostgebirg', 'Ebenwald', 'Silberthal', 'Steinreich', 'Hinterland', 'Dämmerwald', 'Frostgrenze']
    ritter_rang = ['Hochadel', 'Vassal', 'Bauernritter', 'Erbritter', 'Freier Ritter', 'Landritter', 'Schwertbruder', 'Königsritter', 'Tafelritter', 'Schildbruder']
    dorf_namen = ['Eisenwald', 'Drachenhain', 'Sturmfeld', 'Nachtweide', 'Hohenwacht', 'Greifenau', 'Eichental', 'Flammenhöhe', 'Weidenbach', 'Löwenhain']
    
    def random_date(start_year=1000, end_year=1200):
        """Hilfsfunktion zum Erzeugen eines zufälligen Datums im Jahr"""
        return f"{random.randint(start_year, end_year)}-01-01"

    # Könige einfügen
    for name in koenige_namen:
        thronbeginn = random_date(1000, 1050)
        thronende = random_date(1051, 1100)
        cursor.execute('''
        INSERT INTO Koenige (name, thronbeginn, thronende)
        VALUES (?, ?, ?)
        ''', (name, thronbeginn, thronende))

    # Burgen einfügen
    for i in range(10):
        name = burgen_namen[i]
        ort = burgen_orte[i]
        erbaut_im = random.randint(900, 1100)
        koenig_id = random.randint(1, 10)  
        cursor.execute('''
        INSERT INTO Burgen (name, ort, erbaut_im, koenig_id)
        VALUES (?, ?, ?, ?)
        ''', (name, ort, erbaut_im, koenig_id))

    # Ritter einfügen, mit geheimem Passwort
    for i in range(10):
        name = f"Ritter {i+1}"
        rang = random.choice(ritter_rang)
        geburtsjahr = random.randint(950, 1050)
        burg_id = random.randint(1, 10)
        geheimes_passwort = generate_secret_phrase()  # Generiere geheimes Passwort für jeden Ritter
        cursor.execute('''
        INSERT INTO Ritter (name, rang, geburtsjahr, burg_id, geheimes_passwort)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, rang, geburtsjahr, burg_id, geheimes_passwort))

    # Dörfer einfügen
    for i in range(10):
        name = dorf_namen[i]
        bewohnerzahl = random.randint(50, 200)
        burg_id = random.randint(1, 10) 
        cursor.execute('''
        INSERT INTO Doerfer (name, bewohnerzahl, burg_id)
        VALUES (?, ?, ?)
        ''', (name, bewohnerzahl, burg_id))

    # Schlachten einfügen
    for i in range(10):
        schlacht_name = f"Schlacht {i+1}"
        datum = random_date(1050, 1100)
        burg_1_id = random.randint(1, 10)
        burg_2_id = random.randint(1, 10)
        sieger_burg_id = random.choice([burg_1_id, burg_2_id])
        cursor.execute('''
        INSERT INTO Schlachten (name, datum, burg_1_id, burg_2_id, sieger_burg_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (schlacht_name, datum, burg_1_id, burg_2_id, sieger_burg_id))

    # Ritter-Schlachten einfügen
    for ritter_id in range(1, 11):
        for schlacht_id in range(1, 11):
            rolle = random.choice(['Angreifer', 'Verteidiger'])
            cursor.execute('''
            INSERT INTO Ritter_Schlachten (ritter_id, schlacht_id, rolle)
            VALUES (?, ?, ?)
            ''', (ritter_id, schlacht_id, rolle))

    # Armeen einfügen
    for ritter_id in range(1, 11):
        anzahl = random.randint(50, 150)
        cursor.execute('''
        INSERT INTO Armeen (ritter_id, anzahl)
        VALUES (?, ?)
        ''', (ritter_id, anzahl))

    conn.commit()
    conn.close()

@anvil.server.callable
def print_database():
    conn = get_connection()
    cursor = conn.cursor()

    tables = ['Koenige', 'Burgen', 'Ritter', 'Doerfer', 'Schlachten', 'Ritter_Schlachten', 'Armeen']
    
    for table in tables:
        print(f"\n{'='*40}\nTabelle: {table}\n{'='*40}")
      
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        if rows:
            columns = [description[0] for description in cursor.description]
            print(f"{' | '.join(columns)}")
            print('-' * 40) 
            for row in rows:
                print(f"{' | '.join(map(str, row))}")
        else:
            print(f"Keine Daten in der Tabelle {table}.")
        print(f"{'='*40}\n")
    
    conn.close()

import sqlite3

@anvil.server.callable
def check_login(username, password, disable_sql=False):
    if disable_sql:
        return "SQL-Abfragen sind deaktiviert."  # Antwort im Falle von deaktivierten SQL-Abfragen
    try:
        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect('mittelalter.db')
        cursor = conn.cursor()

        # SQL-Abfrage zur Überprüfung des Benutzers
        query = f"SELECT * FROM Ritter WHERE name = '{username}' AND geheimes_passwort = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        conn.close()

        # Wenn ein Benutzer gefunden wurde, erfolgreich anmelden
        if user:
            return True
        else:
            return "Ungültiger Benutzername oder Passwort."  # Benutzername oder Passwort sind falsch

    except sqlite3.Error as e:
        # SQLite Fehler abfangen und Fehlermeldung zurückgeben
        return f"SQL Fehler: {str(e)}"  # Gibt den von SQLite erzeugten Fehler aus

@anvil.server.callable
def get_ritter_info(username):
    conn = sqlite3.connect('mittelalter.db')
    cursor = conn.cursor()

    query = '''
    SELECT Ritter.name, Ritter.rang, Ritter.geburtsjahr, Ritter.geheimes_passwort, Burgen.name AS burg_name
    FROM Ritter
    JOIN Burgen ON Ritter.burg_id = Burgen.id
    WHERE Ritter.name = ?
    '''
    cursor.execute(query, (username,))
    ritter = cursor.fetchone()
    conn.close()
    
    if ritter:
        return {
            'name': ritter[0],
            'rang': ritter[1],
            'geburtsjahr': ritter[2],
            'geheimes_passwort': ritter[3],
            'burg_name': ritter[4]
        }
    else:
        return None