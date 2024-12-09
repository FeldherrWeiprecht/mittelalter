import anvil.server
import sqlite3
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

# Feste geheime Passwörter für die Ritter
def get_fixed_secret_phrases():
    return [
        'Geheim1', 'Geheim2', 'Geheim3', 'Geheim4', 'Geheim5', 
        'Geheim6', 'Geheim7', 'Geheim8', 'Geheim9', 'Geheim10'
    ]

@anvil.server.callable
def fill_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Feste Werte für die Daten
    koenige_namen = ['Aldric', 'Berengar', 'Willelm', 'Thorin', 'Oswin', 'Eldric', 'Lothar', 'Georg', 'Erik', 'Sigurd']
    burgen_namen = ['Drachenstein', 'Eisenwall', 'Felsenburg', 'Goldberg', 'Eisenschmiede', 'Schattenburg', 'Burg der Ahnen', 'Sturmfels', 'Hohenstein', 'Weißhorn']
    burgen_orte = ['Nordreich', 'Südmark', 'Westland', 'Ostgebirg', 'Ebenwald', 'Silberthal', 'Steinreich', 'Hinterland', 'Dämmerwald', 'Frostgrenze']
    ritter_rang = ['Hochadel', 'Vassal', 'Bauernritter', 'Erbritter', 'Freier Ritter', 'Landritter', 'Schwertbruder', 'Königsritter', 'Tafelritter', 'Schildbruder']
    dorf_namen = ['Eisenwald', 'Drachenhain', 'Sturmfeld', 'Nachtweide', 'Hohenwacht', 'Greifenau', 'Eichental', 'Flammenhöhe', 'Weidenbach', 'Löwenhain']

    # Festgelegte Daten für jedes Feld
    koenige_daten = [
        ('Aldric', '1001-01-01', '1050-12-31'),
        ('Berengar', '1010-01-01', '1060-12-31'),
        ('Willelm', '1020-01-01', '1070-12-31'),
        ('Thorin', '1030-01-01', '1080-12-31'),
        ('Oswin', '1040-01-01', '1090-12-31'),
        ('Eldric', '1050-01-01', '1100-12-31'),
        ('Lothar', '1060-01-01', '1110-12-31'),
        ('Georg', '1070-01-01', '1120-12-31'),
        ('Erik', '1080-01-01', '1130-12-31'),
        ('Sigurd', '1090-01-01', '1140-12-31')
    ]

    burgen_daten = [
        ('Drachenstein', 'Nordreich', 1001, 1),
        ('Eisenwall', 'Südmark', 1020, 2),
        ('Felsenburg', 'Westland', 1030, 3),
        ('Goldberg', 'Ostgebirg', 1040, 4),
        ('Eisenschmiede', 'Ebenwald', 1050, 5),
        ('Schattenburg', 'Silberthal', 1060, 6),
        ('Burg der Ahnen', 'Steinreich', 1070, 7),
        ('Sturmfels', 'Hinterland', 1080, 8),
        ('Hohenstein', 'Dämmerwald', 1090, 9),
        ('Weißhorn', 'Frostgrenze', 1100, 10)
    ]

    ritter_daten = [
        ('Ritter 1', 'Hochadel', 1005, 1),
        ('Ritter 2', 'Vassal', 1015, 2),
        ('Ritter 3', 'Bauernritter', 1025, 3),
        ('Ritter 4', 'Erbritter', 1035, 4),
        ('Ritter 5', 'Freier Ritter', 1045, 5),
        ('Ritter 6', 'Landritter', 1055, 6),
        ('Ritter 7', 'Schwertbruder', 1065, 7),
        ('Ritter 8', 'Königsritter', 1075, 8),
        ('Ritter 9', 'Tafelritter', 1085, 9),
        ('Ritter 10', 'Schildbruder', 1095, 10)
    ]

    dorf_daten = [
        ('Eisenwald', 150, 1),
        ('Drachenhain', 200, 2),
        ('Sturmfeld', 250, 3),
        ('Nachtweide', 300, 4),
        ('Hohenwacht', 350, 5),
        ('Greifenau', 400, 6),
        ('Eichental', 450, 7),
        ('Flammenhöhe', 500, 8),
        ('Weidenbach', 550, 9),
        ('Löwenhain', 600, 10)
    ]

    # Liste der festen Passwörter für die Ritter
    fixed_secret_phrases = get_fixed_secret_phrases()

    # Könige einfügen
    for name, thronbeginn, thronende in koenige_daten:
        cursor.execute('''
        INSERT INTO Koenige (name, thronbeginn, thronende)
        VALUES (?, ?, ?)
        ''', (name, thronbeginn, thronende))

    # Burgen einfügen
    for name, ort, erbaut_im, koenig_id in burgen_daten:
        cursor.execute('''
        INSERT INTO Burgen (name, ort, erbaut_im, koenig_id)
        VALUES (?, ?, ?, ?)
        ''', (name, ort, erbaut_im, koenig_id))

    # Ritter einfügen, mit festem geheimen Passwort
    for i, (name, rang, geburtsjahr, burg_id) in enumerate(ritter_daten):
        geheimes_passwort = fixed_secret_phrases[i]  # Verwende das vordefinierte Passwort
        cursor.execute('''
        INSERT INTO Ritter (name, rang, geburtsjahr, burg_id, geheimes_passwort)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, rang, geburtsjahr, burg_id, geheimes_passwort))

    # Dörfer einfügen
    for name, bewohnerzahl, burg_id in dorf_daten:
        cursor.execute('''
        INSERT INTO Doerfer (name, bewohnerzahl, burg_id)
        VALUES (?, ?, ?)
        ''', (name, bewohnerzahl, burg_id))

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

@anvil.server.callable
def check_login(username, password, disable_sql=False):
    if disable_sql:
        return "SQL-Abfragen sind deaktiviert."  # Antwort im Falle von deaktivierten SQL-Abfragen
    try:
        conn = sqlite3.connect('mittelalter.db')
        cursor = conn.cursor()

        # SQL-Abfrage zur Überprüfung des Benutzers
        query = f"SELECT * FROM Ritter WHERE name = '{username}' AND geheimes_passwort = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        conn.close()

        if user:
            return True  # Anmeldung erfolgreich
        else:
            return "Ungültiger Benutzername oder Passwort."  # Fehlerfall

    except sqlite3.Error as e:
        return f"SQL Fehler: {str(e)}"  # Gibt den von SQLite erzeugten Fehler aus

@anvil.server.callable
def get_ritter_data(username):
    try:
        conn = sqlite3.connect('mittelalter.db')
        cursor = conn.cursor()

        # Abfrage, um die Ritterdaten basierend auf dem Benutzernamen zu erhalten
        cursor.execute('''
            SELECT name, rang, geburtsjahr, burg_id, geheimes_passwort 
            FROM Ritter 
            WHERE name = ?
        ''', (username,))
        
        ritter_data = cursor.fetchone()
        
        if ritter_data:
            name, rang, geburtsjahr, burg_id, geheimes_passwort = ritter_data
            
            # Jetzt den Namen der Burg abfragen
            cursor.execute('''
                SELECT name FROM Burgen WHERE id = ?
            ''', (burg_id,))
            
            burg_name = cursor.fetchone()
            if burg_name:
                burg_name = burg_name[0]  # Der Name der Burg ist das erste Element im Tuple

            conn.close()
            
            return name, rang, geburtsjahr, burg_name, geheimes_passwort
        else:
            conn.close()
            return None
    except sqlite3.Error as e:
        print(f"SQL Fehler: {str(e)}")
        return None
