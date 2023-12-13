import matplotlib.pyplot as plt
from matplotlib import cm
import pickle
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

for year in range(2021, 2022):
    # Open pickle file for a given storm year
    with open(f"Data/{year}data.pkl", 'rb') as f:
        x = pickle.load(f)

    # Loop through each storm
    for dict in x:
        
        # set up the figure for each storm
        fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        ax.set_title(f"{dict}")
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
                if (x[dict][key][hrout]['Dissipated?'] == True):
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

            # Adding gridlines with labels
            gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False)
            gl.top_labels = False  # Disable labels at the top
            gl.right_labels = False  # Disable labels at the right
            gl.left_labels = True  # Enable labels on the left
            gl.bottom_labels = True  # Enable labels on the bottom


            # Set the extent to the range you want to display
            ax.set_extent([lon_arr[0]-25, lon_arr[0]+25, lat_arr[0]-25, lat_arr[0]+25], crs=ccrs.PlateCarree())

        plt.show()
        




