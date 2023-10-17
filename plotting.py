import matplotlib.pyplot as plt
import pickle
import numpy as np
import re

for year in range(2018, 2019):

    # open pickle file for a given storm year
    f = open(f"{year}data.pkl", 'rb')
    x = pickle.load(f)
    f.close()


    # loop through each storm
    for dict in x:
        fig, ax = plt.subplots()
        plt.title(f"{dict}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()


        for key in x[dict].keys():
            # initialize np array of x values for plotting (lon is the longitude value, lat is latitude), one for each forecast
            lat_arr = []
            lon_arr = []
            for hrout in x[dict][key].keys():
                lat = x[dict][key][hrout]['Latitude']
                lon = x[dict][key][hrout]['Longitude']
                if (lat[-1] != "N") & (lon[-1] != "W") & (lon[-1] != "E") & (lat[-1] != "S"):
                    break
                if (lat[-1] == "N"):
                    lat_arr.append(float(lat[0:-1]))
                elif (lat[-1] == "S"):
                    lat_arr.append(-float(lat[0:-1]))   
                if (lon[-1] == "E"):
                    lon_arr.append(float(lon[0:-1]))
                elif (lon[-1] == "W"):
                    lon_arr.append(-float(lon[0:-1]))


                # print(dict + ", " + key + ", " + hrout)
                # print(lat + ", " + lon)
            print(dict + ", " + key + ": ")
            print(lat_arr)
            print(lon_arr)
            plt.plot(lon_arr, lat_arr)
            

        plt.show()

        









    
#     for dict in x:
#         print(dict)


# x['AL012015']['1']['INIT']['Latitude']