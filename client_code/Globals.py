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
filename = 'KL_Tageswerte_Beschreibung_Stationen.txt'
ws_loaded = False
regions_loaded = False
obs_loaded = False
regions = {'a', 'b', 'c'}
weather_stations = {}
observations = {}
