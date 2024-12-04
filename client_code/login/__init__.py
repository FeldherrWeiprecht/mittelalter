from ._anvil_designer import loginTemplate
from anvil import *
import anvil.server
from .account import account  # Falls das Formular in einer separaten Datei ist

class login(loginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        anvil.server.call('reset_database')
        anvil.server.call('create_database')
        anvil.server.call('fill_database')

    def submit_button_click(self, **event_args):
        username = self.username.text
        password = self.password.text
        disable_sql = self.disable_sql.checked  # Wert der Checkbox
        
        # Überprüfen, ob Benutzername und Passwort ausgefüllt sind
        if not username or not password:
            self.status_label.text = "Bitte Benutzername und Passwort eingeben."
            return
        
        if disable_sql:
            self.status_label.text = "SQL-Abfragen sind deaktiviert."
        else:
            # Andernfalls normaler Login-Check
            if anvil.server.call('check_login', username, password):
                self.status_label.text = "Erfolgreich eingeloggt!"
                # Nach erfolgreichem Login das Account-Formular öffnen
                self.open_account_form(username)
            else:
                self.status_label.text = "Ungültiger Benutzername oder Passwort."

    def open_account_form(self, username):
        # Account-Formular instanziieren und anzeigen
        account_form = account(username=username)  # Dein Account-Formular
        #self.content_panel.clear()  # Vorheriges Formular löschen, falls nötig
       # self.content_panel.add_component(account_form)  # Formular hinzufügen
