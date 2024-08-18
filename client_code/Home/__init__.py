from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

#import Timer
#>>> numbers = [7, 6, 1, 4, 1, 8, 0, 6]
#>>> with Timer(text="{:.8f}"):
#...     set(numbers)

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if not Globals.ws_loaded:
      print("downloading weather stations...")
      #Globals.regions = anvil.server.call('get_table_data')
      #regions = anvil.server.call('get_region')#, callback=self.populate_dropdown)
      Globals.weather_stations = anvil.server.call('dl_to_weather_stations')
      Globals.ws_loaded = True
      print(type(Globals.weather_stations))
      for key in Globals.weather_stations.keys():
        print(key)
      self.regionDropdown.items =Globals.regions      
      Notification('downloaded',style='info',timeout=2).show()
      self.region_label.visible = True
    else:
      print("regions already loaded.")

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

#  def button_1_click(self, **event_args):
#    """This method is called when the button is clicked"""
#    self.regionDropdown.visible = True
#    regions = anvil.server.call('get_region')#, callback=self.populate_dropdown)
#    self.regionDropdown.items = regions
#    self.region_label.visible = True
    

