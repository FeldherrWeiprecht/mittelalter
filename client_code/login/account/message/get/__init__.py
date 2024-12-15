from ._anvil_designer import getTemplate
from anvil import *
import anvil.server



from ._anvil_designer import getTemplate
from anvil import *
import anvil.server

class get(getTemplate):
    def __init__(self, **properties):
        # Initialisierung der Komponenten
        self.init_components(**properties)

        # URL-Hash auslesen
        url_hash = get_url_hash()  # Liest den Hash-Teil der URL aus (z.B. "?text=KhoorZhoo&d_src=cc")
        
        # Standardwerte setzen, falls kein Hash vorhanden ist
        if not url_hash:
            set_url_hash("text=KhoorZhoo&d_src=sc")  # Standard-Hash setzen
            url_hash = get_url_hash()  # Aktualisierten Hash erneut auslesen

        # Hash-Parameter parsen
        url_params = self.parse_url_hash(url_hash)

        # Werte auslesen
        text = url_params.get("text", "Kein Text")
        d_src = url_params.get("d_src", "sc")  # Standardwert für d_src ist 'sc'

        # Verarbeitung der Parameter
        if d_src == "cc":
            # Text entschlüsseln
            decrypted_text = self.decrypt_text(text)
            self.status_label.text = f"Entschlüsselter Text: {decrypted_text}"
        elif d_src == "sc":
            # Verschlüsselten Text anzeigen
            self.status_label.text = f"Verschlüsselter Text: {text}"
        else:
            self.status_label.text = "Fehler: Ungültiger Parameterwert für 'd_src'."

    def parse_url_hash(self, url_hash):
        """
        Parse den Hash-Teil der URL und gib ein Dictionary zurück.
        """
        url_hash = url_hash.lstrip("?")  # Entferne das führende '?'
        params = url_hash.split("&")
        param_dict = {}
        for param in params:
            if "=" in param:
                key, value = param.split("=", 1)
                param_dict[key] = value
        return param_dict

    def decrypt_text(self, encrypted_text):
        """
        Entschlüsselt eine Caesar-Verschlüsselung (Verschiebung um 3).
        """
        shift = 3
        decrypted = ""
        for char in encrypted_text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                decrypted += chr((ord(char) - shift_base - shift) % 26 + shift_base)
            else:
                decrypted += char
        return decrypted
