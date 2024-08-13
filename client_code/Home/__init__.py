from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def regionDropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.region_label.visible = False
    self.wsDropdown.visible = True
    self.ws_label.visible = True
    ws = anvil.server.call('get_ws', self.regionDropdown.selected_value)
    self.wsDropdown.items = ws

  def wsDropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    ws = anvil.server.call('dlObservations', 
                           self.regionDropdown.selected_value,
                           self.wsDropdown.selected_value)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    regions = anvil.server.call('get_region')#, callback=self.populate_dropdown)
    self.regionDropdown.items = regions
    self.region_label.visible = True
    

