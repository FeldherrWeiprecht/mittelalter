from ._anvil_designer import getTemplate
from anvil import *
import anvil.server


class get(getTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def prove_button_click(self, **event_args):
    if Ture:
      pass