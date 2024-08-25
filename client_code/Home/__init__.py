from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
from .. import Globals

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    print(Globals.region)
    
    # Fill dropdown component for region selection
    if not Globals.weather_stations_loaded:
      url = url = Globals.url + Globals.recent_path + Globals.filename
      Globals.weather_stations = anvil.server.call('dl_to_weather_stations', url)# Main
      Globals.weather_stations_loaded = True
    Globals.regions = sorted(list(set(Globals.weather_stations['region'])))
    regions = Globals.regions
    regions.insert(0,'<Please select a region>')
    self.region_dropdown.items = regions
    Globals.regions_loaded = True    
    self.region_label.visible = True
  
  def region_dropdown_change(self, **event_args):
    """Activate weather station selection, when region is selected"""
    def get_values_by_condition(list_a, list_b, condition):
      return [b for a, b in zip(list_a, list_b) if a == condition]
    self.weather_stations_dropdown.visible = True
    self.ws_label.visible = True
    Globals.region = self.region_dropdown.selected_value
    ws = get_values_by_condition(Globals.weather_stations['region'], 
                                      Globals.weather_stations['name'], 
                                      Globals.region)
    ws.insert(0,'<Please select a station>')
    self.weather_stations_dropdown.items = ws

  def weather_stations_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.weather_stations_dropdown.selected_value != '<Please select a station>':
      ws = anvil.server.call('dl_observations', 
                            self.region_dropdown.selected_value,
                            self.weather_stations_dropdown.selected_value)

    

