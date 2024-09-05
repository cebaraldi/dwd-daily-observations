import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
#import os.path
#import requests
#from datetime import datetime
import pandas as pd

@anvil.server.callable
def check_file_existence(file_name):
  try:
    with open(anvil.files[file_name], "rb") as f:
        file_content = f.read()
        return True, file_content
  except FileNotFoundError:
    return False, None  

@anvil.server.callable
def dlWeatherStations():
  url = "https://opendata.dwd.de/"
  path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'
  recent_path = path + 'recent/'
  filename = 'KL_Tageswerte_Beschreibung_Stationen.txt' 
  # TEXT Data
  url = url + recent_path + filename
  if not os.path.exists(filename):
    save_as = filename
    # Download from URL
    response = requests.get(url, stream=True)
    # Save to file
    with open(save_as, mode="wb") as file:
      for chunk in response.iter_content(chunk_size=10 * 1024):
        file.write(chunk)
        
def convert_to_number(string_number):
    try:
        return int(string_number)
    except ValueError:
        try:
            return float(string_number)
        except ValueError:
            return None  # Or handle the error differently

def convert_to_date(string_date):
    format_string = "%Y%m%d"
    try:
        return datetime.strptime(string_date, format_string),
    except ValueError:
        return None  # Or handle the error differently

@anvil.server.callable
def add_data():
  filename = 'KL_Tageswerte_Beschreibung_Stationen.txt'
  format_string = "%Y%m%d"
  wsid = []
  date_from = []
  date_to = []
  height = []
  lat = []
  lon = []
  city = []
  region = []
  with open(filename, 'r', encoding='Latin-1') as file:
    next(file)  # Skip the first line
    next(file)  # Skip the second line
    while line := file.readline().rstrip():
      wsid.append(line[0:5])
      date_from.append(line[6:14])
      date_to.append(line[15:23])
      height.append(line[24:42])
      lat.append(line[43:52])
      lon.append(line[53:60])
      city.append(line[61:101].strip())
      region.append(line[102:].strip())
    # dictionary of lists 
    dict = {'wsid': wsid, 'date_from': date_from, 'date_to': date_to, 'height': height, # [m]
            'lat': lat, 'lon': lon, 'name': city, 'region': region} # [°]
    df = pd.DataFrame(dict) #.drop(index=[0,1])
    #print(df.columns)
    # Convert columns
    df['date_from'] = pd.to_datetime(df['date_from']).dt.date
    df['date_to'] = pd.to_datetime(df['date_to']).dt.date
    df['height'] = pd.to_numeric(df['height'], downcast="integer")
    df['lat'] = pd.to_numeric(df['lat'], downcast="float")
    df['lon'] = pd.to_numeric(df['lon'], downcast="float")
    print(df.tail())
#      app_tables.dwd_weatherstations.add_row(wsid=line[0:5],
#                                            dstart=convert_to_date(line[6:14]),
#                                            dend=convert_to_date(line[15:23]),
#                                            height= convert_to_number(line[24:42]),
#                                            lat= convert_to_number(line[43:52]),
#                                            lon= convert_to_number(line[53:60]),
#                                            name=line[61:101].strip(),
#                                            region=line[102:].strip()
#                                            )

  # Iterate over DataFrame rows and insert into Anvil table
  for index, row in df.iterrows():
    row_dict = row.to_dict()
#    print(row_dict)
    app_tables.dwd_weatherstations.add_row(**row_dict)