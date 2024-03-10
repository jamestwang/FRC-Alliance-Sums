import json, requests
import os
from dotenv import load_dotenv

# Load API key environment variable from .env file
load_dotenv()
# Access API key
api_key = os.environ['API_KEY']
response = requests.get('https://www.thebluealliance.com/api/v3/events/2023', params={'X-TBA-Auth-Key': api_key})

# Save this request for a year's events locally, as a json file.
if response.status_code == 200:
    data = response.json()
    with open('data.json', 'w') as file:
        json.dump(data, file)
        print('Data saved successfully.')
else:
    print('Failed to retrieve data. Status code:', response.status_code)