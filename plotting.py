import matplotlib.pyplot as plt
import pickle
import numpy as np

for year in range(2021, 2022):

    # open pickle file for a given storm year
    f = open(f"{year}data.pkl", 'rb')
    x = pickle.load(f)
    f.close()


    # print all data in master dict
    for dict in x:
        for key in x[dict].keys():
            # initialize np array of x values for plotting (lon is the longitude value, lat is latitude), one for each forecast
            lat_arr = []
            lon_arr = []
            for hrout in x[dict][key].keys():
                lat = x[dict][key][hrout]['Latitude']
                lon = x[dict][key][hrout]['Longitude']
                lat_arr.append(lat)
                lon_arr.append(lon)
                # print(dict + ", " + key + ", " + hrout)
                # print(lat + ", " + lon)
            print(dict + ", " + key + ": ")
            print(lat_arr)
            print(lon_arr)

    fig, ax = plt.subplots()
    plt.title("Exponential Regression")
    plt.xlabel("years")
    plt.ylabel("Price")
    plt.plot(lon_arr, lat_arr)









    
#     for dict in x:
#         print(dict)


# x['AL012015']['1']['INIT']['Latitude']