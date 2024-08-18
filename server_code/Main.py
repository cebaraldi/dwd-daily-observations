import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import os.path
import requests
from Tools import *
#import tempfile
import zipfile
from urllib.request import urlretrieve

@anvil.server.callable
def extract_year_from_date(date_value):
  year = date_value.year
  return year
  
@anvil.server.callable
def get_records_for_year(table_name, date_column_name, year):
  """
  Retrieves records from a table where the specified date column's year matches the given year.

  Args:
    table_name (str): The name of the table.
    date_column_name (str): The name of the date column.
    year (int): The target year.

  Returns:
    list: A list of records matching the criteria.
  """
  table = app_tables[table_name]
  records = table.search(**{date_column_name: q.date_extract('year') == year})
  return records
  
@anvil.server.callable
def get_region():
  rows =  app_tables.dwd_weatherstations.search()
  unique_values = set(row['region'] for row in rows)
  sorted_values = sorted(list(unique_values))
  sorted_values.insert(0,"<Please select a region>")
  return sorted_values  

@anvil.server.callable
def get_ws(region):
  rows = app_tables.dwd_weatherstations.search(region=q.ilike(region))
  unique_values = set(row['name'] for row in rows)
  sorted_values = sorted(list(unique_values))
  sorted_values.insert(0,"<Please select a station>")
  return sorted_values

@anvil.server.callable
def dlObservations(region, ws):
  record = app_tables.dwd_weatherstations.search(
    name=q.ilike(ws), 
    region=q.ilike(region)
  )
  url = "https://opendata.dwd.de/"
  path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'
  recent_path = path + 'recent/'
  #historical_path = path + 'historical/'

  for r in record:
    filename = f"tageswerte_KL_{r['wsid']}_akt.zip"
    #print(filename)
    # BINARY Data
    url = url + recent_path + filename
    print(url, filename)

#    if not os.path.exists(filename):
#      urlretrieve(url, filename)
#      
#      try:
#        with zipfile.ZipFile(filename, mode="r") as archive:
#          for file in archive.namelist():
#            if file.endswith("/tmp/produkt_klima_tag_*.txt"):
#              archive.extract(file, ".")
#              print(file)
#      except FileNotFoundError:
#        return False

@anvil.server.callable
def dl_to_weather_stations():
  url = "https://opendata.dwd.de/"
  path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'
  recent_path = path + 'recent/'
  filename = 'KL_Tageswerte_Beschreibung_Stationen.txt' 
  # TEXT Data
  url = url + recent_path + filename
#  if not os.path.exists(filename):
#    save_as = filename
#    # Download from URL
#    response = requests.get(url, stream=True)
#    # Save to file
#    with open(save_as, mode="wb") as file:
#      for chunk in response.iter_content(chunk_size=10 * 1024):
#        file.write(chunk)
  response = requests.get(url)
  print(response)
  print(type(response))
  return(response)