from ._anvil_designer import HomeTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
from datetime import datetime
from .. import Globals

def extract_observables(self):
  # Zip into a list of tuples
  zl = list(zip(Globals.weather_stations['wsid'], #0
                Globals.weather_stations['name'], #1
                Globals.weather_stations['region'], #2
                Globals.weather_stations['date_from'], #3
                Globals.weather_stations['date_to'] #4
                ))
  found_tuple = [t for t in zl if t[1] == Globals.weather_station and t[2] == Globals.region]
  wsid = found_tuple[0][0]
  date_from = found_tuple[0][3]
  date_to = found_tuple[0][4]

  if not Globals.observations_loaded :
    with Notification(f'Downloading observations of {Globals.weather_station}, please wait...'):
      data = anvil.server.call('dl_zip', wsid, date_from, date_to, 
                              self.cb_recent.checked, 
                              self.cb_historical.checked
                              )
      Globals.observations_loaded =  True
  obsdate = data['MESS_DATUM']

  # Do plot w/ multiple observables on the server side (plotly on client cannot )
  #tmin = data['TNK']
  #tmax = data['TXK']
  if self.rb_temperature.selected:
    yval = data['TMK']
    ylabel = 'Temperature [℃]'
  if self.rb_precipitation.selected:
    yval = data['RSK']
    ylabel = 'Precipitation [mm]'
  if self.rb_snowcover.selected:
    yval = data['SHK_TAG']
    ylabel = 'Snow Cover [cm]'
  if self.rb_ground_temperature.selected:
    yval = data['TGK']
    ylabel = 'Precipitation [℃]'
  if self.rb_vapor_pressure.selected:
    yval = data['VPM']
    ylabel = 'Vapor Pressure [hPa]'
  if self.rb_pressure.selected:
    yval = data['PM']
    ylabel = 'Air Pressure [hPa]'
  if self.rb_humidity.selected:
    yval = data['UPM']
    ylabel = 'Realative Humidity [%]'
  if self.rb_sunshine.selected:
    yval = data['SDK']
    ylabel = 'Sunshine Duration [h]'

  if not self.cb_statistics.checked:
    scatter_plot(self, wsid, ylabel, obsdate, yval)
  else:
    pass

  
def scatter_plot(self, wsid, ylabel, obsdate, yval):
      # Plotly: plotting with go.Figure()
      x = strings_to_dates(obsdate, date_format="%Y%m%d")
      y = replace_negative_999(strings_to_floats(yval))
      count = sum(1 for e in y if e is not None)
      if count == 0:
        Notification('No observations available!',  style="warning").show()
    
      # Specify the layout
      layout = go.Layout(
        title=go.layout.Title(text=f'{wsid} - {Globals.weather_station} / {Globals.region}', x=0.5),
        xaxis_title='Date',
        yaxis_title=ylabel
      )
          
      # Make the scatter plot
      fig = go.Figure(data=go.Scatter(x=x, y=y), layout=layout)
  
      # Display the plot in an Anvil Plot component (client side)
      self.plot_1.figure = fig  

def strings_to_dates(string_list, date_format="%Y-%m-%d"):  # Adjust date format as needed
  date_list = []
  for string_value in string_list:
    try:
      date_value = datetime.strptime(string_value, date_format).date()
      date_list.append(date_value)
    except ValueError:
      # Handle invalid dates, e.g., log an error or skip the value
      print(f"Error converting '{string_value}' to date with format {date_format}")
  return date_list
  
def strings_to_floats(string_list):
  float_list = []
  for string_value in string_list:
    try:
      float_value = float(string_value)
      float_list.append(float_value)
    except ValueError:
      # Handle invalid values, e.g., log an error or skip the value
      print(f"Error converting '{string_value}' to float")
  return float_list

def replace_negative_999(data):
  """Replaces -999 values in a list with None.

  Args:
    data: A list of float values.

  Returns:
    A new list with -999 values replaced by None.
  """
  return [value if value != -999 else None for value in data]

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # debug
    print(); Globals.check_globals()
    
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
    self.stations_dropdown.enabled = True
    Globals.weather_station = '<Please select a station>'
    #print(f'selected region = {self.region_dropdown.selected_value}')
    Globals.region = self.region_dropdown.selected_value
    ws = get_values_by_condition(Globals.weather_stations['region'], 
                                      Globals.weather_stations['name'], 
                                      Globals.region)

    # debug
    print(); Globals.check_globals()
    
    self.stations_dropdown.placeholder = '<Please select a station>'
    self.stations_dropdown.items = ws

  def stations_dropdown_change(self, **event_args):
    Globals.weather_station = self.stations_dropdown.selected_value
    Globals.observations_loaded =  False

    # debug
    print()
    Globals.check_globals()    

    extract_observables(self)
    
    # debug
    Globals.check_globals()

  def rb_temperature_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_temperature_clicked')

  def rb_precipitation_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_precipitation_clicked')
    

  def rb_snowcover_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_snowcover_clicked')

  def rb_ground_temperature_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_ground_temperature_clicked')

  def rb_vapor_pressure_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_vapor_pressure_clicked')

  def rb_pressure_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_pressure_clicked')

  def rb_humidity_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_humidity_clicked')

  def rb_sunshine_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    print('rb_sunshine_clicked')

  def cb_recent_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    print('cb_recent_change')

  def cb_historical_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    print('cb_historical_change')

  def cb_statistics_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    print('cb_statistics_change')
