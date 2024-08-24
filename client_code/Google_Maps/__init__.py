from ._anvil_designer import Google_MapsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Google_Maps(Google_MapsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Fill dropdown component for region selection
    Globals.regions = sorted(list(set(Globals.weather_stations['region'])))
    self.drop_down_region.items = Globals.regions
    self.drop_down_region.placeholder = '<Please select a region>'
    self.markers = {}

    # Center to map of germany
    lat = 51.3
    lon = 9.4
    zoom = 6.2
    self.map_of_germany.center = GoogleMap.LatLng(lat, lon)
    self.map_of_germany.zoom = zoom

  def drop_down_region_change(self, **event_args):
    """This method is called when an item is selected"""
    def get_values_by_condition(list_a, list_b, condition):
      return [b for a, b in zip(list_a, list_b) if a == condition]
    Globals.region =self.drop_down_region.selected_value
    if Globals.region is not None:
      name = get_values_by_condition(Globals.weather_stations['region'], 
                                        Globals.weather_stations['name'], 
                                        Globals.region)
      lat = get_values_by_condition(Globals.weather_stations['region'], 
                                  Globals.weather_stations['lat'], 
                                  Globals.region)
      lon = get_values_by_condition(Globals.weather_stations['region'], 
                                  Globals.weather_stations['lon'], 
                                  Globals.region)
      height = get_values_by_condition(Globals.weather_stations['region'], 
                                  Globals.weather_stations['height'], 
                                  Globals.region)
      green_icon = GoogleMap.Icon(
            url="http://maps.google.com/mapfiles/kml/paddle/grn-blank.png"
          )
    
      for n, lat, lon, h in zip(name, lat, lon, height):
        #print(f'{n} {lat} {lon} {h}')
        marker = GoogleMap.Marker(
          animation=GoogleMap.Animation.DROP,
          position=GoogleMap.LatLng(lat, lon),
          icon = green_icon
        )     
        self.markers[marker]=f'{n}\n{h}'
        def marker_click(sender, **event_args):
          i = GoogleMap.InfoWindow(content=Label(text=self.markers[sender]))
          i.open(map, sender)
        marker.add_event_handler("click", marker_click)
        self.map_of_germany.add_component(marker)
