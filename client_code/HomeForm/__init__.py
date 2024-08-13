from ._anvil_designer import HomeFormTemplate
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import Notification

class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    regions = anvil.server.call('get_region')#, callback=self.populate_dropdown)
    self.regionDropdown.items = regions
  
  def regionDropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.wsDropdown.visible = True
    ws = anvil.server.call('get_ws', self.regionDropdown.selected_value)
    self.wsDropdown.items = ws

    #notification = Notification("Weather Stations are downloaded", title="Information", style="info")   
    #notification.show()
    #import time
    #time.sleep(15)
    #notification.hide()
    
    #notification = Notification("Weather Stations inserted into DB", title="Information", style="info")   
    #notification.show()

  def wsDropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    ws = anvil.server.call('dlObservations', 
                           self.regionDropdown.selected_value,
                           self.wsDropdown.selected_value)
