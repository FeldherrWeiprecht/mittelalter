from ._anvil_designer import getTemplate
from anvil import *
import anvil.server

class get(getTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        url_hash = get_url_hash()
        if not url_hash:
            set_url_hash("text=KhoorZhoo&d_src=sc")
            url_hash = get_url_hash()

        url_params = self.parse_url_hash(url_hash)
        text = url_params.get("text", "Kein Text")
        d_src = url_params.get("d_src", "sc")

        if d_src == "cc":
            decrypted_text = self.decrypt_text(text)
            self.status_label.text = f"Entschlüsselter Text: {decrypted_text}"
        elif d_src == "sc":
            self.status_label.text = f"Verschlüsselter Text: {text}"
        else:
            self.status_label.text = "Fehler: Ungültiger Parameterwert für 'd_src'."

    def parse_url_hash(self, url_hash):
        url_hash = url_hash.lstrip("?") 
        params = url_hash.split("&")
        param_dict = {}
      
        for param in params:
            if "=" in param:
                key, value = param.split("=", 1)
                param_dict[key] = value
              
        return param_dict

    def decrypt_text(self, encrypted_text):
        shift = 3
        decrypted = ""
      
        for char in encrypted_text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                decrypted += chr((ord(char) - shift_base - shift) % 26 + shift_base)
            else:
                decrypted += char
              
        return decrypted