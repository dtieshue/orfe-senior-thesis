
# code to fix a data entry (such as a typo in the website)
import pickle

year = 2009

# Load the dictionary from the pickle file
with open(f"Data/{year}data.pkl", 'rb') as f:
    x = pickle.load(f)

print(x['EP012009']['6'])
# x['EP012009']['6']['24HR']['Time (UTC)'] = '20/1800Z'

# x['AL022007']['2'] = storm_data = {
#     "INITIAL": {"TOut": "INITIAL", "Time (UTC)": "02/0300Z", "Latitude": "24.7N", "Longitude": "84.9W", "Wind Speed (KT)": "45", "Dissipated?": False},
#     "12HR": {"TOut": "12HR", "Time (UTC)": "02/1200Z", "Latitude": "27.3N", "Longitude": "84.0W", "Wind Speed (KT)": "40", "Dissipated?": False},
#     "24HR": {"TOut": "24HR", "Time (UTC)": "03/0000Z", "Latitude": "30.0N", "Longitude": "82.5W", "Wind Speed (KT)": "35", "Dissipated?": False},
#     "36HR": {"TOut": "36HR", "Time (UTC)": "03/1200Z", "Latitude": "33.0N", "Longitude": "80.5W", "Wind Speed (KT)": "30", "Dissipated?": False},
#     "48HR": {"TOut": "48HR", "Time (UTC)": "04/0000Z", "Latitude": "36.1N", "Longitude": "76.5W", "Wind Speed (KT)": "30", "Dissipated?": False},
#     "72HR": {"TOut": "72HR", "Time (UTC)": "05/0000Z", "Latitude": "42.0N", "Longitude": "70.0W", "Wind Speed (KT)": "30", "Dissipated?": False},
#     "96HR": {"TOut": "96HR", "Time (UTC)": "06/0000Z", "Latitude": "n/a", "Longitude": "n/a", "Wind Speed (KT)": "n/a", "Dissipated?": True}
# }


# x['AL092006']['2'] = {
#     "INITIAL": {"TOut": "INITIAL", "Time (UTC)": "28/0300Z", "Latitude": "27.2N", "Longitude": "53.8W", "Wind Speed (KT)": "30", "Dissipated?": False},
#     "12HR": {"TOut": "12HR", "Time (UTC)": "28/1200Z", "Latitude": "28.2N", "Longitude": "55.0W", "Wind Speed (KT)": "35", "Dissipated?": False},
#     "24HR": {"TOut": "24HR", "Time (UTC)": "29/0000Z", "Latitude": "29.9N", "Longitude": "56.5W", "Wind Speed (KT)": "40", "Dissipated?": False},
#     "36HR": {"TOut": "36HR", "Time (UTC)": "29/1200Z", "Latitude": "31.6N", "Longitude": "57.6W", "Wind Speed (KT)": "45", "Dissipated?": False},
#     "48HR": {"TOut": "48HR", "Time (UTC)": "30/0000Z", "Latitude": "33.6N", "Longitude": "58.1W", "Wind Speed (KT)": "50", "Dissipated?": False},
#     "72HR": {"TOut": "72HR", "Time (UTC)": "01/0000Z", "Latitude": "38.0N", "Longitude": "57.0W", "Wind Speed (KT)": "50", "Dissipated?": False},
#     "96HR": {"TOut": "96HR", "Time (UTC)": "02/0000Z", "Latitude": "42.0N", "Longitude": "52.5W", "Wind Speed (KT)": "50", "Dissipated?": True, "Extratropical": True},
#     "120HR": {"TOut": "120HR", "Time (UTC)": "03/0000Z", "Latitude": "46.0N", "Longitude": "45.0W", "Wind Speed (KT)": "50", "Dissipated?": True, "Extratropical": True}
# }
# # Update the value in the dictionary
# x['AL092006']['14']['48H']['Latitude'] = '61.0N'

# Open the file in write mode (wb) to save the updated dictionary
with open(f"Data/{year}data.pkl", 'wb') as f:
    pickle.dump(x, f)