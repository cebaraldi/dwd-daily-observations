from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Fill dropdown component for region selection
    if not Globals.ws_loaded:
      url = url = Globals.url + Globals.recent_path + Globals.filename
      Globals.weather_stations = anvil.server.call('dl_to_weather_stations', url)# Main
      Globals.ws_loaded = True
    Globals.regions = sorted(list(set(Globals.weather_stations['region'])))
    regions = Globals.regions
    regions.insert(0,'<Please select a region>')
    self.regionDropdown.items = regions
    self.region_label.visible = True

  
  def regionDropdown_change(self, **event_args):
    """Activate weather station selection, when region is selected"""
    def get_values_by_condition(list_a, list_b, condition):
      return [b for a, b in zip(list_a, list_b) if a == condition]
    self.wsDropdown.visible = True
    self.ws_label.visible = True
    ws = get_values_by_condition(Globals.weather_stations['region'], 
                                      Globals.weather_stations['name'], 
                                      self.regionDropdown.selected_value)
    ws.insert(0,'<Please select a region>')
    self.wsDropdown.items = ws

  def wsDropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    ws = anvil.server.call('dlObservations', 
                           self.regionDropdown.selected_value,
                           self.wsDropdown.selected_value)

#  def button_1_click(self, **event_args):
#    """This method is called when the button is clicked"""
#    self.regionDropdown.visible = True
#    regions = anvil.server.call('get_region')#, callback=self.populate_dropdown)
#    self.regionDropdown.items = regions
#    self.region_label.visible = True
    

