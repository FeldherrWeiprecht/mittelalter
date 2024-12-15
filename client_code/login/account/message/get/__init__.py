from ._anvil_designer import getTemplate
from anvil import *
import anvil.server


from anvil import *
import anvil.server

class get(getTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Lese den URL-Hash (alles nach dem #)
        url_hash = get_url_hash()  # Gibt den Hash-Teil der URL zurück (z.B. ?text=KhoorZhoo&d_src=cc)

        # Entferne das '?' und teile die Parameter
        if url_hash:
            url_params = {}

            # Verarbeite die URL-Parameter, falls vorhanden
            for param in url_hash.lstrip('?').split('&'):
                if '=' in param:  # Nur Parameter mit einem '=' behandeln
                    key, value = param.split('=', 1)
                    url_params[key] = value

            # Lese 'text' und 'd_src' aus den URL-Parametern
            text = url_params.get("text", None)
            d_src = url_params.get("d_src", "sc")  # Standardwert für d_src ist 'sc'

            if text and d_src:
                if d_src == 'cc':
                    # Wenn d_src = 'cc', entschlüssle den Text
                    decrypted_text = self.decrypt_text(text)
                    self.status_label.text = f"Entschlüsselter Text: {decrypted_text}"
                else:
                    # Wenn d_src = 'sc', zeige den verschlüsselten Text an
                    self.status_label.text = f"Verschlüsselter Text: {text}"
            else:
                self.status_label.text = "Fehler: Keine gültigen Parameter in der URL."
        else:
            self.status_label.text = "Fehler: Keine URL-Parameter vorhanden."

    def decrypt_text(self, encrypted_text):
        # Entschlüsselung der Nachricht mit einer Caesar-Verschlüsselung (Verschiebung um 3)
        shift = 3
        decrypted = ""
        for char in encrypted_text:
            if char.isalpha():  # Nur Buchstaben entschlüsseln
                shift_base = 65 if char.isupper() else 97
                decrypted += chr((ord(char) - shift_base - shift) % 26 + shift_base)
            else:
                decrypted += char  # Nicht-Buchstaben bleiben unverändert
        return decrypted

    def change_url_hash(self):
        # Beispiel, wie der Hash manuell geändert werden kann
        text = "KhoorZhoo"
        d_src = "cc"  # Der Wert, den du setzen möchtest
        new_url = f"#get?text={text}&d_src={d_src}"
        
        # Ändere den Hash in der URL
        js = f"window.location.hash = '{new_url}';"
        self.call_js(js)
