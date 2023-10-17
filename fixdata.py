
# code to fix a data entry (such as a typo in the website)
import pickle

year = 2016

# Load the dictionary from the pickle file
with open(f"{year}data.pkl", 'rb') as f:
    x = pickle.load(f)

# Update the value in the dictionary
x['AL102016']['14']['48H']['Latitude'] = '61.0N'

# Open the file in write mode (wb) to save the updated dictionary
with open(f"{year}data.pkl", 'wb') as f:
    pickle.dump(x, f)