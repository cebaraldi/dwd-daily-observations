from ._anvil_designer import ContactTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Contact(ContactTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def bt_submit_click(self, **event_args):
    name = 'mujo'
    email = 'mujoa@home.com'
    feedback = 'hello'
    anvil.server.call('send_feedback',name, email, feedback)
