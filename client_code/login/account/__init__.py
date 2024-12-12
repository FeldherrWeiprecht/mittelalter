from ._anvil_designer import accountTemplate
from anvil import *
import anvil.server

class account(accountTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.ritter_name = "Ritter 1"  # Beispielname des Ritters
        self.load_ritter_data()

    def load_ritter_data(self):
        try:
            username = self.ritter_name
            ritter_data = anvil.server.call('get_ritter_data', username)
            
            if ritter_data:
                name, rang, geburtsjahr, burg_name, geheimes_passwort = ritter_data
                self.label_name.text = f"Name: {name}"
                self.label_rang.text = f"Rang: {rang}"
                self.label_geburtsjahr.text = f"Geburtsjahr: {geburtsjahr}"
                self.label_burg_name.text = f"Burg: {burg_name}"
                self.label_geheimes_passwort.text = f"Geheimes Passwort: {geheimes_passwort}"
            else:
                alert("Ritter nicht gefunden!")
        except Exception as e:
            alert(f"Fehler beim Laden der Ritterdaten: {str(e)}")

    def search_button_click(self, **event_args):
        search_username = self.search_box.text
        disable_sql = self.disable_sql.checked  # Abfrage, ob SQL-Injection deaktiviert ist

        if not search_username:
            self.status_label.text = "Bitte einen Benutzernamen eingeben!"
            return
        
        # Aufruf der Funktion, um den Ritter zu suchen
        try:
            # Überprüfung, ob SQL-Injection aktiviert ist
            if disable_sql:
                # SQL-Injection verhindern (sichere Methode)
                result = 0
            else:
                # SQL-Injection zulassen (unsichere Methode)
                result = anvil.server.call('get_highest_rank_ritter_insecure', search_username)
            
            if result:
                name, rang = result
                self.status_label.text = f"Erfolg! Höchster Rang: {rang} - Ritter: {name}"
                open_form('login.account.message')
            elif result == 0:
              self.status_label.text = "SQL-Injection deaktiviert."

            else:
                self.status_label.text = "Fehler: Ritter nicht gefunden."
        
        except Exception as e:
            self.status_label.text = f"Fehler bei der Suche: {str(e)}"

    def logout_button_click(self, **event_args):
        open_form('login')

    def continue_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass
