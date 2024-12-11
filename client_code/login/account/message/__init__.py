from ._anvil_designer import messageTemplate
from anvil import *
import anvil.server


class message(messageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.message_to_send = self.text_area

  def send_button_click(self, **event_args):
    open_form('login.account.message.get')
