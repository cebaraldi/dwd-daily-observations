from ._anvil_designer import HomeTemplate
from anvil import *
import plotly.graph_objects as go
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
    data = anvil.server.call('dl_zip', wsid, date_from, date_to)
    Notification('observations downloaded').show()
    
    print(data.keys())
    obsdate = data['MESS_DATUM']
    tmin = data['TNK']
    tavg = data['TMK']
    tmax = data['TXK']
    print(obsdate)
    print(tavg)
    print(f"Length of mininum temperatue observations is {len(tmin)}")
    print(f"Length of maxinum temperatue observations is {len(tmax)}")

    # Sample data
    #x = [1, 2, 3, 4, 5]
    #y = [2, 4, 5, 4, 5]
    x = strings_to_dates(obsdate, date_format="%Y%m%d")
    #y = strings_to_floats(tavg)
    y = replace_negative_999(strings_to_floats(tavg))
    print(y)

    # Create a Plotly figure
    fig = go.Figure(data=go.Scatter(x=x, y=y))

    # Display the plot in an Anvil Plot component (client side)
    self.plot_1.figure = fig    
