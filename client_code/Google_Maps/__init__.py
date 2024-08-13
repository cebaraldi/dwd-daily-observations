from ._anvil_designer import Google_MapsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Google_Maps(Google_MapsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    lat = 51.3
    lon = 9.4
    zoom = 6.2
    self.map_of_germany.center = GoogleMap.LatLng(lat, lon)
    self.map_of_germany.zoom = zoom

    #app_tables.meteoch_weatherstations
    ws = anvil.server.call('get_read_ws')
    
#  def button_1_click(self, **event_args):
#    """This method is called when the button is clicked"""
#    open_form('Form2')

#set position_markers():

#  marker = GoogleMap.Marker(
#    animation=GoogleMap.Animation.DROP,
#    position=GoogleMap.LatLng(lat, lon)  
#  ) 
  
def position_marker(self, lat, lon):
  marker = GoogleMap.Marker(
    animation=GoogleMap.Animation.DROP,
    position=GoogleMap.LatLng(lat, lon)  
  )  
  self.map_1.add_component(marker)
#  marker.add_event_handler("click", marker_click)
#  def marker_click(sender, **event_args):
#    i = GoogleMap.InfoWindow(content=Label(text=station))
#    i.open(map, sender)
    

  #position_marker(self, 47.541142,	7.583525)
  #position_marker(self, 46.004217,	8.960322)
  #position_marker(self, 47.016631,	9.502594)

  
#  marker2 = GoogleMap.Marker(
#    animation=GoogleMap.Animation.DROP,
#    position=GoogleMap.LatLng(46.004217,	8.960322)  
#  )  
#  self.map_1.add_component(marker2)  
#  marker2.add_event_handler("click", marker2_click)
  
#  marker3 = GoogleMap.Marker(
#    animation=GoogleMap.Animation.DROP,
#    position=GoogleMap.LatLng(47.016631,	9.502594)  
#  )      
#  self.map_1.add_component(marker3)
#  marker3.add_event_handler("click", marker3_click)

#def marker2_click(sender, **event_args):
#  i = GoogleMap.InfoWindow(content=Label(text="This is Lugano!"))
#  i.open(map, sender)
  
#def marker3_click(sender, **event_args):
#  i = GoogleMap.InfoWindow(content=Label(text="This is Bad Ragaz!"))
#  i.open(map, sender)

