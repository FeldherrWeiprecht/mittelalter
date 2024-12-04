from ._anvil_designer import accountTemplate
from anvil import *
import anvil.server

class account(accountTemplate):
    def __init__(self, username, **properties):
        self.init_components(**properties)
        self.username = username
        