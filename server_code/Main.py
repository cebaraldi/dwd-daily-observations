import anvil.server
from datetime import datetime
import os.path
import requests
from Tools import *
import csv
import io
import zipfile
from urllib.request import urlretrieve
import pandas as pd

from contextlib import closing
import json
from bs4 import BeautifulSoup

def get_url_paths(url, ext='', params={}):
  response = requests.get(url, params=params)
  if response.ok:
    response_text = response.text
  else:
    return response.raise_for_status()
  soup = BeautifulSoup(response_text, 'html.parser')
  parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
  return parent
  
#@anvil.server.callable
#def extract_year_from_date(date_value):
#  year = date_value.year
#  return year
  
#@anvil.server.callable
#def get_records_for_year(table_name, date_column_name, year):
#  """
#  Retrieves records from a table where the specified date column's year matches the given year.
#
#  Args:
#    table_name (str): The name of the table.
#    date_column_name (str): The name of the date column.
#    year (int): The target year.
#
#  Returns:
#    list: A list of records matching the criteria.
#  """
#  table = app_tables[table_name]
#  records = table.search(**{date_column_name: q.date_extract('year') == year})
#  return records
  
#@anvil.server.callable
#def get_region():
#  rows =  app_tables.dwd_weatherstations.search()
#  unique_values = set(row['region'] for row in rows)
#  sorted_values = sorted(list(unique_values))
#  sorted_values.insert(0,"<Please select a region>")
#  return sorted_values  

#@anvil.server.callable
#def get_ws(region):
#  rows = app_tables.dwd_weatherstations.search(region=q.ilike(region))
#  unique_values = set(row['name'] for row in rows)
#  sorted_values = sorted(list(unique_values))
#  sorted_values.insert(0,"<Please select a station>")
#  return sorted_values

@anvil.server.callable
def dl_to_weather_stations(url):
  print(url)
  response = requests.get(url)
  if response.status_code == 200:
    lines = response.text.splitlines()
    #format_string = "%Y%m%d"
    wsid = []
    date_from = []
    date_to = []
    height = []
    lat = []
    lng = []
    station = []
    region = []
    abgabe = []
    for line in lines[2:]:
      
      wsid.append(line[0:5])
      date_from.append(line[6:14])
      date_to.append(line[15:23])
      height.append(line[24:38])
      lat.append(line[39:50])
      lng.append(line[51:60])
      station.append(line[61:101].strip()) #.strip())
      region.append(line[102:142].strip()) #.strip())
      abgabe.append(line[143:].strip()) #.strip())
      
#      print(f'{wsid}: {len(wsid)}')
#      print(f'{date_from}: {len(date_from)}')
#      print(f'{date_to}: {len(date_to)}')
#      print(f'{height}: {len(height)}')
#      print(f'{lat}: {len(lat)}')
#      print(f'{lng}: {len(lng)}')
#      print(f'{station}: {len(station)}')
#      print(f'{region}: {len(region)}')

    
    # dictionary of lists 
    dict = {'wsid': wsid, 'date_from': date_from, 'date_to': date_to, 'height': height, # [m]
            'lat': lat, 'lng': lng, 'name': station, 'region': region, 'abgabe': abgabe}
    df = pd.DataFrame(dict) #.drop(index=[0,1])
    # Convert columns
    df['date_from'] = pd.to_datetime(df['date_from']).dt.date
    df['date_to'] = pd.to_datetime(df['date_to']).dt.date
    df['height'] = pd.to_numeric(df['height'], downcast="integer")
    df['lat'] = pd.to_numeric(df['lat'], downcast="float")
    df['lng'] = pd.to_numeric(df['lng'], downcast="float")
    # remove stations w/ missing latest observation
    df1 = df[df['date_to']==df['date_to'].max()]
    # remove stations where abgabe is not 'Frei'
    df2 = df1[df1['abgabe']=='Frei']
  return(df2.to_dict('list'))

@anvil.server.callable
def dl_observations(wsid, date_from, date_to):
  url = "https://opendata.dwd.de/"
  path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'
  recent_path = path + 'recent/'
  #historical_path = path + 'historical/'

  recent_filename = f'tageswerte_KL_{wsid}_akt.zip'
  #historical_filename = f'tageswerte_KL_{wsid}_{date_from}_{date_to}_hist.zip'
  
  # BINARY Data
  print(url + recent_path, recent_filename)
  #print(url + historical_path, historical_filename)

  if not os.path.exists(recent_filename):
    urlretrieve(url, recent_filename)
    
    try:
      with zipfile.ZipFile(recent_filename, mode="r") as archive:
        for file in archive.namelist():
          if file.endswith("/tmp/produkt_klima_tag_*.txt"):
            archive.extract(file, ".")
            print(file)
    except FileNotFoundError:
      return False

def dict_to_dataframe(data_dict):
  """Converts a dictionary with a binary string value into a Pandas DataFrame.

  Args:
    data_dict: The input dictionary.

  Returns:
    A Pandas DataFrame.
  """
  value = next(iter(data_dict.values()))  # Extract the value
  decoded_value = value.decode('utf-8')  # Decode the byte string
  records = decoded_value.strip().split('eor\r\n')
  data = [record.split(';') for record in records]
  # Trim column names using strip()
  df = pd.DataFrame(data[1:], columns=(s.strip() for s in data[0]))
  df = df[df.columns[:-1]]
  # Remove leading and trailing spaces from all columns
  df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)  
  return(df)  
  
@anvil.server.callable
def dl_zip(wsid, date_from, date_to, recent, historical):
  if not recent and not historical:
    recent = True
  
  url = "https://opendata.dwd.de/"
  path = 'climate_environment/CDC/observations_germany/climate/daily/kl/'

  if recent:
    recent_path = path + 'recent/'
    filename = f"tageswerte_KL_{wsid}_akt.zip"
    url_recent = url + recent_path + filename
    body = {}
    r = requests.get(url_recent)
    with closing(r), zipfile.ZipFile(io.BytesIO(r.content)) as archive:   
      # print({member.filename: archive.read(member) for member in archive.infolist()})
      body ={member.filename: archive.read(member) 
            for member in archive.infolist() 
            if (member.filename.startswith('produkt_klima_tag_'))
            }
    rdf = dict_to_dataframe(body)
    print(rdf.shape)
    if not historical:
      hdf = rdf[0:0]
  if historical:  
    historical_path = path + 'historical/'
    #filename = f"tageswerte_KL_{wsid}_{date_from.strftime('%Y%m%d') }_{date_to.strftime('%Y%m%d') }_hist.zip"
    #url_historical = url + historical_path + filename
    url_historical = url + historical_path
    #print(url_historical)

    pattern = f"tageswerte_KL_{wsid}_{date_from.strftime('%Y%m%d') }_"
    #print(pattern)
    ext = 'zip'
    file_list = get_url_paths(url_historical, ext)
    #print(file_list)
    found = [s for s in file_list if pattern in s]
    if len(found) > 0:
      url = found[0]
      
    body = {}
    r = requests.get(url)
    with closing(r), zipfile.ZipFile(io.BytesIO(r.content)) as archive:   
      # print({member.filename: archive.read(member) for member in archive.infolist()})
      body ={member.filename: archive.read(member) 
            for member in archive.infolist() 
            if (member.filename.startswith('produkt_klima_tag_'))
            }
    hdf = dict_to_dataframe(body)
    print(hdf.shape)
    if not recent:
      rdf = hdf[0:0]
    print('---')
  df = pd.concat([rdf, hdf])
  print()  
  df = rdf.drop('STATIONS_ID', axis=1) # already given as parameter
  dict_list = df.to_dict('list')
  return(dict_list)

#@anvil.server.callable
#def get_observations(ws, current=True, historical=False):
#  rows = app_tables.meteoch_weatherstations.search(station=q.ilike(ws))
#  if current:
#    urlcurry = list(set(row['urlcurry'] for row in rows))[0]
#    cws = pd.read_csv(urlcurry, sep=";", header=0, encoding = "latin_1").dropna()
#    if not historical:
#      pws = cws[0:0]
#  if historical:
#    urlprevy = list(set(row['urlprevy'] for row in rows))[0]
#    pws = pd.read_csv(urlprevy, sep=";", header=0, encoding = "latin_1").dropna()
#    if not current:
#      cws = pws[0:0]
# df = pd.concat([cws, pws])
# dict_list = df.to_dict('list')
#  return(dict_list)