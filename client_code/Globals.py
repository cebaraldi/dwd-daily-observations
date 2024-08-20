import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Globals
#
url = 'https://opendata.dwd.de/'
path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'
recent_path = path + 'recent/'
historical_path = path + 'historical/'
filename = 'KL_Tageswerte_Beschreibung_Stationen.txt'

#regions_loaded = False

region = None
weather_station = None
weather_stations = {}
weather_stations_loaded = False

observations = {}
observations_loaded = False