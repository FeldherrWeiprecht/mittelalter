from ._anvil_designer import messageTemplate
from anvil import *
import anvil.server

class message(messageTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def send_click(self, **event_args):
        # Nachricht aus dem Textfeld abrufen
        text = self.text_area.text

        if not text:  # Prüfen, ob Text leer ist
            self.status_label.text = "Bitte eine Nachricht in der Textbox eingeben."
        elif text.startswith('cc') and len(text) > 2:  # Prüfen, ob Nachricht mit 'cc' beginnt
            self.status_label.text = "Erfolgreich zugestellt."

            # Verschlüsselung durchführen
            encrypted_text = self.encrypt_text(text)

            # Übergabe an die Ziel-Form mit verschlüsseltem Text und d_src=sc (Standard)
            open_form('login.account.message.get', text=encrypted_text, d_src="sc")

        else:
            self.status_label.text = "Fehler: Überprüfe, ob die Nachricht mit 'cc' anfängt und dann Inhalt folgt."

    def encrypt_text(self, text):
        # Einfache Caesar-Verschlüsselung (Verschiebung um 3)
        shift = 3
        encrypted = ""
        for char in text:
            if char.isalpha():  # Nur Buchstaben verschlüsseln
                shift_base = 65 if char.isupper() else 97
                encrypted += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            else:
                encrypted += char  # Nicht-Buchstaben bleiben unverändert
        return encrypted
