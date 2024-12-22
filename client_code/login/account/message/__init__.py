from ._anvil_designer import messageTemplate
from anvil import *
import anvil.server

class message(messageTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def send_click(self, **event_args):
        text = self.text_area.text
        if not text: 
            self.status_label.text = "Bitte eine Nachricht in der Textbox eingeben."
        elif text.startswith('cc') and len(text) > 2:
            self.status_label.text = "Erfolgreich zugestellt."
            encrypted_text = self.encrypt_text(text)
            open_form('login.account.message.get', text=encrypted_text, d_src="sc")
        else:
            self.status_label.text = "Fehler: Überprüfe, ob die Nachricht mit 'cc' anfängt und dann Inhalt folgt."

    def encrypt_text(self, text):
        shift = 3
        encrypted = ""
      
        for char in text:
            if char.isalpha(): 
                shift_base = 65 if char.isupper() else 97
                encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            else:
                encrypted += char
              
        return encrypted