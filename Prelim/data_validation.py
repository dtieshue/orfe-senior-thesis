# file to ensure that the data in each dictionary is correctly represented and in the right format
# to be coded


# All storms for a range of years
import pickle

for year in range(2020, 2021):
    # Open pickle file for a given storm year
    with open(f"Data/{year}data.pkl", 'rb') as f:
        x = pickle.load(f)

    # Loop through each storm
    for dict in x:
        
        for i, key in enumerate(x[dict].keys()):
        
            for hrout in x[dict][key].keys():
                lat = x[dict][key][hrout]['Latitude']
                lon = x[dict][key][hrout]['Longitude']
                print("HROUT:", hrout)
                print("LAT,LON:", lat, ",", lon)


storm_codes = [
    "AL022015", "EP162015", "EP202015", "EP222015", 
    "AL042016", 
    "AL032017", "AL072017", "AL092017", "AL132017", "AL162017", "EP182017", 
    "AL012018", "AL072018", "EP032018", "EP192018", "EP202018", "EP212018", "EP232018", "EP242018", 
    "AL022019", "AL072019", "AL112019", "AL162019", "AL172019", "EP152019", "EP162019", 
    "AL032020", "AL082020", "AL132020", "AL142020", "AL192020", "AL222020", "AL262020", "AL282020", 
    "AL032021", "AL062021", "AL072021", "AL092021", "AL142021", "EP042021", "EP142021", "EP162021", "EP172021"
]

for storm in storm_codes:
    # one storm in a year
    year = int(storm[-4:])
    # Open pickle file for a given storm year
    with open(f"Data/{year}data.pkl", 'rb') as f:
        x = pickle.load(f)

    # Loop through each storm
    dict = storm
        
    for i, key in enumerate(x[dict].keys()):

        print(key)
        for hrout in x[dict][key].keys():
            lat = x[dict][key][hrout]['Latitude']
            lon = x[dict][key][hrout]['Longitude']
            print("HROUT:", hrout)
            print("LAT,LON:", lat, ",", lon)
            print("WS", x[dict][key][hrout]['Wind Speed (KT)'])

                    


            



