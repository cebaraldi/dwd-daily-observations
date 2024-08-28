from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
from .. import Globals

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # debug
    Globals.check_globals()
    
    # Download weather stations and fill dropdown component for region selection
    if not Globals.weather_stations_loaded:
      url = url = Globals.url + Globals.recent_path + Globals.filename
      Globals.weather_stations = anvil.server.call('dl_to_weather_stations', url)# Main
      Globals.weather_stations_loaded = True
    Globals.regions = sorted(list(set(Globals.weather_stations['region'])))
    self.region_dropdown.items = Globals.regions  
    self.region_dropdown.placeholder = '<Please select a region>'

    # debug
    Globals.check_globals()
  
  def region_dropdown_change(self, **event_args):
    def get_values_by_condition(list_a, list_b, condition):
      return [b for a, b in zip(list_a, list_b) if a == condition]
    self.weather_stations_dropdown.enabled = True
    #print(f'selected region = {self.region_dropdown.selected_value}')
    Globals.region = self.region_dropdown.selected_value
    ws = get_values_by_condition(Globals.weather_stations['region'], 
                                      Globals.weather_stations['name'], 
                                      Globals.region)

    # debug
    Globals.check_globals()
    
    #ws.insert(0,'<Please select a station>')
    print('fill weather_stations_dropdown')
    self.weather_stations_dropdown.placeholder = '<Please select a station>'
    self.weather_stations_dropdown.items = ws

  def weather_stations_dropdown_change(self, **event_args):
    Globals.weather_station = self.weather_stations_dropdown.selected_value
    print()
    # debug
    Globals.check_globals()    
    print(Globals.weather_stations.keys())
    # Zip into a list of tuploes
    zl = list(zip(Globals.weather_stations['wsid'], 
                  Globals.weather_stations['name'],
                  Globals.weather_stations['region'],
                  Globals.weather_stations['date_from'],
                  Globals.weather_stations['date_to']
                 ))
    found_tuple = [t for t in zl if t[1] == Globals.weather_station and t[2] == Globals.region]
    wsid = found_tuple[0][0]
    date_from = found_tuple[0][3]
    date_to = found_tuple[0][4]
    ws = anvil.server.call('dl_observations', wsid, date_from, date_to)

