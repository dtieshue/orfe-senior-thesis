import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

year = 2017
with open(f"Data/{year}data.pkl", 'rb') as f:
    x = pickle.load(f)

dict = 'AL092017'

# set up the figure for each storm
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# set title
ax.set_title(f"{dict}")

# add map features
ax.coastlines()
ax.add_feature(cfeature.OCEAN, zorder=0)
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')

# initialize variables to calculate centroid of all points
latsum = 0
lonsum = 0
tot = 0

for i, key in enumerate(x[dict].keys()):
    # Initialize np array of x values for plotting (lon is the longitude value, lat is latitude), one for each forecast
    lat_arr = []
    lon_arr = []

    for hrout in x[dict][key].keys():
        tot = tot + 1
        lat = x[dict][key][hrout]['Latitude']
        lon = x[dict][key][hrout]['Longitude']
        if (lat[-1] != "N") & (lon[-1] != "W") & (lon[-1] != "E") & (lat[-1] != "S"):
            break
        if (lat[-1] == "N"):
            lat_arr.append(float(lat[0:-1]))
            latsum = latsum + float(lat[0:-1])
        elif (lat[-1] == "S"):
            lat_arr.append(-float(lat[0:-1]))
            latsum = latsum - float(lat[0:-1])
        if (lon[-1] == "E"):
            lon_arr.append(float(lon[0:-1]))
            lonsum = lonsum + float(lon[0:-1])
        elif (lon[-1] == "W"):
            lon_arr.append(-float(lon[0:-1]))
            lonsum = lonsum - float(lon[0:-1])

    ## Customize Plotting ##
    # Create a colormap to represent the increasing brightness
    colormap = cm.plasma
    color = colormap((i % 12)/12)

    # mark starting point for each forecast
    ax.plot(lon_arr[0], lat_arr[0], marker="o", color=color)

    # plotting the forecasts
    ax.plot(lon_arr, lat_arr,
            color=color, linewidth=2,
            transform=ccrs.Geodetic(),)

# plot city of interest
ax.plot(-95.3698, 29.7604, marker="*", color='c', markersize=10)
ax.plot(-80.1918, 25.7617, marker="o", color='r', markersize=1)
ax.plot(-76.8099, 18.0179, marker="o", color='r', markersize=1)

latmean = latsum / tot
lonmean = lonsum / tot
print(latmean)
print(lonmean)

# Adding gridlines with labels
gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False)
gl.top_labels = False  # Disable labels at the top
gl.right_labels = False  # Disable labels at the right
gl.left_labels = True  # Enable labels on the left
gl.bottom_labels = True  # Enable labels on the bottom

# Set the extent to the range you want to display
ax.set_extent([lonmean-25, lonmean+25, latmean-25, latmean+25], crs=ccrs.PlateCarree())

plt.show()
