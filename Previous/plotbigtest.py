import matplotlib.pyplot as plt
import pickle
import numpy as np
import re


fig, ax = plt.subplots()

# Load the image using plt.imread and provide the correct file path
# map = plt.imread('/Users/dylantieshue/Documents/GitHub/orfe-senior-thesis/map1.png')
# plt.imshow(map, extent=[-165, 190, -75, 150])
plt.title("All plots on the same graph")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
# plt.legend()

bigs = []

for year in range(2015, 2022):
    # open pickle file for a given storm year
    f = open(f"Data/{year}data.pkl", 'rb')
    x = pickle.load(f)
    f.close()

    # loop through each storm
    for dict in x:
        for key in x[dict].keys():
            # initialize np array of x values for plotting (lon is the longitude value, lat is latitude), one for each forecast
            lat_arr = []
            lon_arr = []
            for hrout in x[dict][key].keys():
                lat = x[dict][key][hrout]['Latitude']
                lon = x[dict][key][hrout]['Longitude']
                if (lat[-1] != "N") & (lat[-1] != "S") & (lon[-1] != "E") & (lon[-1] != "W"):
                    break
                if (lat[-1] == "N"):
                    lat_arr.append(float(lat[0:-1]))
                elif (lat[-1] == "S"):
                    lat_arr.append(-float(lat[0:-1]))
                if (lon[-1] == "E"):
                    lon_arr.append(float(lon[0:-1]))
                elif (lon[-1] == "W"):
                    lon_arr.append(-float(lon[0:-1]))
                
                if -float(lon[0:-1]) > 100:
                    print("Greater")
                    bigs.append(dict + key)
                # print(dict + ", " + key + ", " + hrout)
                # print(lat + ", " + lon)
            print(dict + ", " + key + ": ")
            print(lat_arr)
            print(lon_arr)
            plt.plot(lon_arr, lat_arr, label =f'{dict}, {key}')
            

plt.show()
print(bigs)
        









    
#     for dict in x:
#         print(dict)


# x['AL012015']['1']['INIT']['Latitude']
# x['AL102016']['14']['48H']['Latitude']

