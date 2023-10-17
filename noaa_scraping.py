import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# define function to extract text content from a URL
def extract_text_from_url(url, start_keyword, end_keyword):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # extract text from HTML
        text_content = soup.get_text().upper()

        # find position of the start keyword and end keyword
        start_keyword_position = text_content.find(start_keyword)
        end_keyword_position = text_content.find(end_keyword)

        if start_keyword_position != -1 and end_keyword_position != -1:
            relevant_text = text_content[start_keyword_position:end_keyword_position]
            return relevant_text
        else:
            print(f'Start or end keyword not found in {url}')
            raise Exception("Keyword error")
            return None
    else:
        print(f'Failed to fetch content from {url}')
        return None

# create dictionary to store all of the info
master_dict = {}

# loop through each year *** NO 2023, no pre-2003
for year in range(2015, 2017):

  # *********************************** comment out if putting data from mutliple years in one dict ***************************************
  master_dict = {}

  # provide website data of NOAA archive for each year
  url = f'https://www.nhc.noaa.gov/archive/{year}'
  print(year)
  response = requests.get(url)

  # getting the links to each storm for a given year, based on a pattern in the position of the links
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    found_arc1 = False
    found_arc2 = False
    found_cyc = False
    storm_urls = []
    for link in links:
      # print(link.get('href'))
      if found_cyc:
        break;
      elif link.get('href') == '/cyclones/':
        found_cyc = True
        break;
      elif found_arc2:
        # print(link.get('href'))
        href = link.get('href')
        storm_urls.append(f'https://www.nhc.noaa.gov/archive/{year}/{href}')
      elif found_arc1 & (link.get('href') == '/archive/2023/') :
        found_arc2 = True
      elif link.get('href') == '/archive/2023/':
        found_arc1 = True
      else:
        continue;
  else:
    print('Failed to retrieve the webpage.')

  storm_name = ""
  # loop through each storm for a given year
  for url in storm_urls:
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # if needed use code to extract a specific pattern for the links
        links = soup.find_all('a', href=re.compile(r''))
        adv_urls = []

        for link in links:
          href = link.get('href')
          if href != None:
            if href.__contains__('discus'):
              full_url = f"https://www.nhc.noaa.gov{href}"
              adv_urls.append(full_url)
              print(full_url)

    else:
        print('Failed to retrieve the webpage.')


    # list of all advisory discussion urls
    urls_to_read = adv_urls

    # specify words to start and end with in the text
    start_keyword = "DISCUSSION"
    end_keyword = f" {year}"
    start_keyword2 = "FORECAST POSITIONS AND MAX WINDS"
    end_keyword2 = "$"

    storm_dict = {}
    i = 1


    # loop through the discussion urls
    for url in urls_to_read:
        name_datetime = extract_text_from_url(url, start_keyword, end_keyword)
        loc_speed = extract_text_from_url(url, start_keyword2, end_keyword2)

        name_datetime_arr = name_datetime.split("\n")
        loc_speed_arr = loc_speed.split("\n")[2:]
        while("" in loc_speed_arr):
          loc_speed_arr = [s for s in loc_speed_arr if s.strip()]

        disc_num = name_datetime_arr[0]
        disc_num = re.sub(r'[^0-9]', '', disc_num)
        # disc_num = disc_num[-1]


        line2 = name_datetime_arr[1].split()
        storm_name = line2[-1]
        print(storm_name)

        print(f'Content from {url}:\n')
        if name_datetime:
            print(f'Date/Time: \n{name_datetime_arr}\n')
        if loc_speed:
            # Process or print the text content as needed
            print(f'Location/Direction/Speed:\n{loc_speed_arr}')

        # storm_name = name_datetime

        # initialize an empty list to store the data for a particular advisory
        parsed_data = {}

        # loop through each individual line in the selected string for a given advisory
        for line in loc_speed_arr:
            parts = line.split()

            if parts[0] == "INITIAL":
              parts[0] = "INIT"


            # check if a line indicates that the storm has dissipated
            if parts[1].find("DISSIPATED") != -1:
              data_dict = {
                  'TOut': parts[0],
                  'Time (UTC)': parts[1][0:7],
                  'Latitude': "n/a",
                  'Longitude': "n/a",
                  'Wind Speed (KT)': "n/a",
                  'Dissipated?' : True
              }

            # check if a line indicates that the storm has dissipated
            elif len(parts[1]) > 8:
              data_dict = {
                  'TOut': parts[0],
                  'Time (UTC)': parts[1][0:7],
                  'Latitude': "n/a",
                  'Longitude': "n/a",
                  'Wind Speed (KT)': "n/a",
                  'Dissipated?' : True
              }

            # check if the line in the advisory is complete
            elif len(parts) >= 6:
              time = parts[0]
              date = parts[1]
              lat = parts[2]
              lon = parts[3]
              wind_speed = parts[4]

              # create a dictionary
              data_dict = {
                  'TOut': time,
                  'Time (UTC)': date,
                  'Latitude': lat,
                  'Longitude': lon,
                  'Wind Speed (KT)': wind_speed,
                  'Dissipated?' : False
                  # Add more key-value pairs here if needed
              }


              # add the data to the advisory dictionary
            parsed_data[data_dict['TOut']] = data_dict

        # add the advisory's dictionary information to the storm dictionary
        # storm_dict[disc_num] = parsed_data
        storm_dict[f'{i}'] = parsed_data
        i = i + 1
        print(parsed_data)



  # add the storm's dictionary information to the master dictionary
    master_dict[storm_name] = storm_dict
    # print("storm:")
    # print(storm_dict)



################################################################################################################################################################################################################################################


  # saving the data to a pickle file
  # load pickle module
  import pickle

  # define dictionary
  # dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}

  # create a binary pickle file 
  f = open(f"{year}data.pkl","wb")

  # write the python object (dict) to pickle file
  pickle.dump(master_dict,f)

  # close file
  f.close()

  # f = open("2021data.pkl", 'rb')

  # x = pickle.load(f)

  # f.close()

  # print(x)


