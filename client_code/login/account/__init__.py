from ._anvil_designer import accountTemplate
from anvil import *
import anvil.server

class account(accountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Any code you write here will run before the form opens.