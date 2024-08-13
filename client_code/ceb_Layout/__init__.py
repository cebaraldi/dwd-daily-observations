from ._anvil_designer import ceb_LayoutTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ceb_Layout(ceb_LayoutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def google_maps_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Google_Maps')

  def about_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('About')

  def contact_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Contact')
