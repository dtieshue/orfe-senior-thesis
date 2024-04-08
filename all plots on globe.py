import matplotlib.pyplot as plt
from matplotlib import cm
import pickle
import cartopy.crs as ccrs
import cartopy.feature as cfeature

for year in range(2018, 2019):
    # Open pickle file for a given storm year
    with open(f"Data/{year}data.pkl", 'rb') as f:
        x = pickle.load(f)

    # Set up the globe projection with adjusted parameters
    projection = ccrs.Orthographic(-100, 37)  # Central longitude and latitude
    fig, ax = plt.subplots(subplot_kw={'projection': projection})
    plt.title(f"All Plots {year}")
    ax.coastlines()
    ax.add_feature(cfeature.OCEAN, zorder=0)
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')

    # Adjust the extent of the map view
    ax.set_global()
    ax.gridlines()

    # Loop through each storm
    for storm in x:
        for i, forecast in enumerate(x[storm].keys()):
            lat_arr = []
            lon_arr = []

            for hrout in x[storm][forecast].keys():
                lat = x[storm][forecast][hrout]['Latitude']
                lon = x[storm][forecast][hrout]['Longitude']
                if lat[-1] == "N":
                    lat_arr.append(float(lat[:-1]))
                elif lat[-1] == "S":
                    lat_arr.append(-float(lat[:-1]))
                if lon[-1] == "E":
                    lon_arr.append(float(lon[:-1]))
                elif lon[-1] == "W":
                    lon_arr.append(-float(lon[:-1]))

            # Create a colormap to represent the increasing brightness
            colormap = cm.plasma
            color = colormap(i / len(x[storm]))

            # Plotting the storm track
            ax.plot(lon_arr, lat_arr, color=color, linewidth=2, transform=ccrs.Geodetic())

    plt.show()
