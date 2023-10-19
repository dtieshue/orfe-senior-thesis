import matplotlib.pyplot as plt
import numpy as np

import cartopy.crs as ccrs
import cartopy.feature as cfeature




fig = plt.figure()



## Customize Plotting ##
# Create a colormap to represent the increasing brightness
colormap = cm.plasma
color = colormap(i / len(x[dict]))

# # plot values on xy plane (not transformed)
# plt.plot(lon_arr, lat_arr, color=color)
# mark starting point for each forecast
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(lon_arr[0], lat_arr[0]))
ax.add_feature(cfeature.OCEAN, zorder=0)
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')


ax.set_global()
ax.gridlines()
ax.plot(lon_arr[0], lat_arr[0], marker = "o", color = color)

# plotting the forecasts
ax.plot(lon_arr, lat_arr,
color=color, linewidth=2,
transform=ccrs.Geodetic(),)  


plt.show()

