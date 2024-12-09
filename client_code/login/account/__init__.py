from ._anvil_designer import accountTemplate
from anvil import *
import anvil.server

class account(accountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    # Hier setzen wir den Ritternamen direkt. Du kannst diesen Namen auch dynamisch über ein Textfeld setzen.
    self.ritter_name = "Ritter 1"  # Beispielname des Ritters
    
    # Lade die Ritter-Daten basierend auf dem Namen
    self.load_ritter_data()

  def load_ritter_data(self):
    try:
        # Verwende den festen Ritter-Namen oder lasse ihn vom Benutzer eingeben
        username = self.ritter_name  # Hier könnte auch ein Eingabefeld verwendet werden
        
        # Rufe die Ritter-Daten aus der Datenbank ab
        ritter_data = anvil.server.call('get_ritter_data', username)
        
        if ritter_data:
            # Angenommene Ritter-Datenstruktur: (name, rang, geburtsjahr, burg_name, geheimes_passwort)
            name, rang, geburtsjahr, burg_name, geheimes_passwort = ritter_data
            
            # Setze die Labels mit den abgerufenen Werten
            self.label_name.text = f"Name: {name}"
            self.label_rang.text = f"Rang: {rang}"
            self.label_geburtsjahr.text = f"Geburtsjahr: {geburtsjahr}"
            self.label_burg_name.text = f"Burg: {burg_name}"  # Burg-Name anzeigen
            self.label_geheimes_passwort.text = f"Geheimes Passwort: {geheimes_passwort}"
        else:
            # Wenn keine Daten gefunden wurden
            alert("Ritter nicht gefunden!")
    except Exception as e:
        alert(f"Fehler beim Laden der Ritterdaten: {str(e)}")
