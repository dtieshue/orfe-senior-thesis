
# print all 2020 data in master dict, with latitude and longitude
for dict in master_dict:
  if dict[4:].__contains__('2020'):
    print(dict)
    for key in master_dict[dict].keys():
      print(master_dict[dict][key]['INIT']['Latitude'] + ", " + master_dict[dict][key]['INIT']['Longitude'])


# print all data in master dict
for dict in master_dict:
    print(dict)


# open pickle file, check all data
import pickle
year = 2021
f = open(f"{year}data.pkl", 'rb')

x = pickle.load(f)

f.close()

# print all data in master dict
for dict in master_dict:
    print(dict)

print(x)


