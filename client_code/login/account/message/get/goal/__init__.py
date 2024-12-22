from ._anvil_designer import goalTemplate
from anvil import *
import anvil.server

class goal(goalTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)