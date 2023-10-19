import matplotlib.pyplot as plt
from matplotlib import cm
import pickle
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

for year in range(2018, 2019):
    # Open pickle file for a given storm year
    with open(f"Data/{year}data.pkl", 'rb') as f:
        x = pickle.load(f)

    # Loop through each storm
    for dict in x:

        # set up the figure for each storm
        fig, ax = plt.subplots()
        plt.title(f"{dict}")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        ax = plt.axes(projection=ccrs.Orthographic(-100, 37))
        ax.coastlines()
        ax.add_feature(cfeature.OCEAN, zorder=0)
        ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')

        for i, key in enumerate(x[dict].keys()):
            # Initialize np array of x values for plotting (lon is the longitude value, lat is latitude), one for each forecast
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


            ## Customize Plotting ##
            # Create a colormap to represent the increasing brightness
            colormap = cm.plasma
            color = colormap(i / len(x[dict]))

            # # plot values on xy plane (not transformed)
            # plt.plot(lon_arr, lat_arr, color=color)
            # mark starting point for each forecast
            ax.plot(lon_arr[0], lat_arr[0], marker = "o", color = color)
            # plotting the forecasts
            ax.plot(lon_arr, lat_arr,
            color=color, linewidth=2,
            transform=ccrs.Geodetic(),)  


            # # setting ax view range values
            # ax.set_xlim(float(min(lon_arr))-25, float(max(lon_arr))+25)
            # ax.set_ylim(float(min(lat_arr))-25, float(max(lat_arr))+25)
            ax.set_global()

        plt.show()
        

