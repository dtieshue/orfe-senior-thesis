import matplotlib.pyplot as plt
import pickle
from dateutil import parser
import re
from matplotlib import cm
import numpy as np
from math import sin, cos, sqrt, atan2, radians


# function to check if date/time matches format
def check_pattern(input_string, pattern):

    if re.match(pattern, input_string):
        return True
    else:
        return False
    
# assert(check_pattern(p, r"\d{2}/\d{4}Z") == True) ## test

# function to define the hurricane score
def wind_speed(distance, v_m, r_m):

    b = 2
    x = 0
    s = 0.5
    x = ((r_m/distance)**b)*np.exp(1-(r_m/distance)**b)

    return v_m*x**s

# function to calculate distance using lat, lon (distance in km)
def distance(loc1, loc2):
    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(loc1[0])
    lon1 = radians(loc1[1])
    lat2 = radians(loc2[0])
    lon2 = radians(loc2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

# define set of functions to predict Rmax8
def calc_f(lat):
    return 2*.00007292*sin(radians(lat))

def calc_mratio(v_max, r_175, lat):
    return 0.699 * np.exp(-0.00618*(v_max - 17.5)-0.00210*(v_max - 17.5)*(1/2*calc_f(lat)*r_175))

def calc_m175(r_175, lat):
    return r_175 * 17.5 + 1/2 * calc_f(lat)*r_175**2

def calc_rmax(v_max, r_175, lat):
    return v_max/(calc_f(lat))*(sqrt(1+2*calc_f(lat)*(calc_m175(r_175, lat)*calc_mratio(v_max, r_175, lat))/(v_max**2))-1)


# storm_codes = [
#     "AL022015", "EP162015", "EP202015", "EP222015", 
#     "AL042016", 
#     "AL032017", "AL072017", "AL092017", "AL132017", "AL162017", "EP182017", 
#     "AL012018", "AL072018", "EP032018", "EP192018", "EP202018", "EP212018", "EP232018", "EP242018", 
#     "AL022019", "AL072019", "AL112019", "AL162019", "AL172019", "EP152019", "EP162019", 
#     "AL032020", "AL082020", "AL132020", "AL142020", "AL192020", "AL222020", "AL262020", "AL282020", 
#     "AL032021", "AL062021", "AL072021", "AL092021", "AL142021", "EP042021", "EP142021", "EP162021", "EP172021"
# ]

storm_codes = ['AL092017']

for storm in storm_codes:
    year = int(storm[-4:])

    with open(f"Data/{year}data.pkl", 'rb') as f:
        x = pickle.load(f)

    dict = storm
    houston = np.array([29.7604, -95.3698]) # define the lat lon values for houston
    nola = np.array([29.9511, -90.0715]) # define the lat lon values for new orleans
    test = np.array([14.1, -70.3698]) # define the lat lon values for test city
    miami = np.array([25.7617,-80.1918]) # define the lat lon values for miami

    print(x[dict]['1']['INIT']['Latitude'])
    time = list('29/0300Z')
    p = '01/0900Z'



    # set up the figure for each storm
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title(f"{dict}")
    plt.xlabel("Hours Since Inception")
    plt.ylabel("Wind Speed")

    day_count = 0
    prev28 = 0
    prev29 = 0
    prev30 = 0
    prev31 = 0
    base_day = list(x[dict]['1']['INIT']['Time (UTC)'])[0:2]
    base_day = [int(base_day[0]), int(base_day[1])]


    for i, key in enumerate(x[dict].keys()):
        times = [] # temporary until I have final formula for the threat score
        wind_speeds = []
        lat_arr = []
        lon_arr = []
        hscore_arr = []

        for j, key2 in enumerate(x[dict][key].keys()):
        
            print(key, key2) # for debugging

            if (x[dict][key][key2]['Dissipated?'] != True):

                lat = x[dict][key][key2]['Latitude']
                lon = x[dict][key][key2]['Longitude']
                ws_temp = x[dict][key][key2]['Wind Speed (KT)']   
                
                # only add time if it is not dissipated
                time_string = list(x[dict][key][key2]['Time (UTC)']) # need to include timing later
                # times.append((2*j + i) * 6)


                
                current_day = [int(time_string[0]), int(time_string[1])]
                add31 = 0
                if ((current_day[0] - base_day[0])*10 + (current_day[1] - base_day[1])) < 0:
                    if prev_day == [3,1]:
                        prev31 = 1
                    elif prev_day == [3,0]:
                        prev30 = 1
                    elif prev_day == [2,9]:
                        prev29 = 1
                    elif prev_day == [2,8]:
                        prev28 = 1
                    
                    adds = prev28 * 28 + prev29 * 29 + prev30 * 30 + prev31 * 31
                    day_hrs = ((current_day[0] - base_day[0])*10 + (current_day[1] - base_day[1]) + adds)* 24
                    hour = int(time_string[3]) * 10 + int(time_string[4]) + day_hrs
                    print(hour)
                    times.append(hour)
                else:
                    day_hrs = ((current_day[0] - base_day[0])*10 + (current_day[1] - base_day[1]))* 24
                    hour = int(time_string[3]) * 10 + int(time_string[4]) + day_hrs
                    print(hour)
                    times.append(hour)
            
                wind_speeds.append(int(ws_temp))

                if (lat[-1] == "N"):
                    lat_arr.append(float(lat[0:-1]))
                elif (lat[-1] == "S"):
                    lat_arr.append(-float(lat[0:-1]))
                if (lon[-1] == "E"):
                    lon_arr.append(float(lon[0:-1]))
                elif (lon[-1] == "W"):
                    lon_arr.append(-float(lon[0:-1]))
                city = houston
                dist = distance(city, np.array([lat_arr[-1], lon_arr[-1]]))
                # print("the distance is", dist) # for debugging
                windspeed_ms = int(ws_temp) * 0.5144 # change from knots to m/s
                hscore_arr.append(wind_speed(dist, windspeed_ms, calc_rmax(windspeed_ms, 60, lat_arr[-1]))) # calculate
                prev_day = current_day

        print(times)
        print(wind_speeds)
        print(lat_arr)
        print(lon_arr)
        print(hscore_arr)

        colormap = cm.tab20
        color = colormap(i / len(x[dict]))


        
        # plotting the forecasts
        ax.plot(times[0], hscore_arr[0], marker = "o", color = color)
        ax.plot(times, hscore_arr, color=color, label = key)
        ax.legend()


    plt.show()



