from ._anvil_designer import loginTemplate
from anvil import *
import anvil.server

class login(loginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        anvil.server.call('reset_database')
        anvil.server.call('create_database')
        anvil.server.call('fill_database')

    def submit_button_click(self, **event_args):
      username = self.username.text
      password = self.password.text
      disable_sql = self.disable_sql.checked  
      
      if not username or not password:
          self.status_label.text = "Bitte Benutzername und Passwort eingeben!"
          return
      
      if disable_sql:
          self.status_label.text = "SQL-Abfragen sind deaktiviert."
      else:
          result = anvil.server.call('check_login', username, password)
          if result == True:
              self.status_label.text = "Erfolgreich eingeloggt!"
              open_form('login.account')
          else:
              self.status_label.text = f"Fehler: {result}"  