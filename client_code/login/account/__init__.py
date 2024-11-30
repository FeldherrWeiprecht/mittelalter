from ._anvil_designer import accountTemplate
from anvil import *
import anvil.server

class account(accountTemplate):
    def __init__(self, username, **properties):
        self.init_components(**properties)
        self.username = username
        self.load_ritter_info()

    def load_ritter_info(self):
        # Abrufen der Ritterdaten basierend auf dem Benutzernamen
        ritter = anvil.server.call('get_ritter_info', self.username)
        
        if ritter:
            # Daten in die Labels laden
            self.label_name.text = ritter['name']
            self.label_rang.text = ritter['rang']
            self.label_burg.text = ritter['burg_name']
            self.label_geburtsjahr.text = str(ritter['geburtsjahr'])
            self.label_geheimes_passwort.text = ritter['geheimes_passwort']
        else:
            self.label_name.text = "Daten nicht gefunden"
            self.label_rang.text = ""
            self.label_burg.text = ""
            self.label_geburtsjahr.text = ""
            self.label_geheimes_passwort.text = ""
