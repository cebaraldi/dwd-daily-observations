import anvil.server

# Goolge map centered on DE
de_lat = 51.3
de_lon = 9.4
de_zoom = 6.2

# DWD url
url = 'https://opendata.dwd.de/'
path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'
recent_path = path + 'recent/'
historical_path = path + 'historical/'
filename = 'KL_Tageswerte_Beschreibung_Stationen.txt'

# Dictionary for region dropdown component
regions = {}
regions_loaded = False

# Dictionaries for weather station and observation data
weather_stations = {}
weather_stations_loaded = False
observations = {}
observations_loaded = False

# Dropdown selection status and selected values
region = None
#region_selected = False !=None
weather_station = None
#weather_station_selected = False !=None

def check_globals():
  print(f'region = {region}: region_selected = {region_selected}')
  print(f'weather_station = {weather_station}: weather_station_selected = {weather_station_selected}')
  print(f'regions_loaded: {regions_loaded}')
  print(f'weather_stations_loaded = {weather_stations_loaded}')
  print(f'observations_loaded = {observations_loaded}')