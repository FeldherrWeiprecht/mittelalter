from ._anvil_designer import messageTemplate
from anvil import *
import anvil.server

class message(messageTemplate):
  def __init__(self, **properties):
    # Initialisierung der Komponenten
    self.init_components(**properties)
  def send_click(self, **event_args):
    # Nachricht aus dem Textfeld abrufen
    text = self.text_area.text
    
    if not text:  # Prüfen, ob Text leer ist
      self.status_label.text = "Bitte eine Nachricht in der Textbox eingeben."
    elif text.startswith('cc') and len(text) > 2:  # Prüfen, ob Nachricht mit 'cc' beginnt
      self.status_label.text = "Erfolgreich zugestellt."
      open_form('login.account.message.get')
    else:
      self.status_label.text = "Fehler: Überprüfe, ob die Nachricht mit 'cc' anfängt und dann Inhalt folgt."
