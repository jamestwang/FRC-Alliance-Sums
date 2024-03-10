import json, requests, time
import numpy as np
import os
from dotenv import load_dotenv

# Load API key environment variable from .env file
load_dotenv()
# Access API key
api_key = os.environ['API_KEY']

# Get every event with match data
for year in range(2002, 2024):
# for year in range(2002, 2003):
    # No matches in 2021
    if (year == 2021):
        continue
    
    # API call for event keys
    event_keys_response = requests.get('https://www.thebluealliance.com/api/v3/events/'+str(year)+'/keys', params={'X-TBA-Auth-Key': api_key})

    # Save this request for a year's events locally, as a json file.
    if event_keys_response.status_code == 200:
        data = event_keys_response.json()
        with open(str(year)+'events.json', 'w') as file:
            json.dump(data, file)
            print(year, 'event keys saved successfully.')
    else:
        print('Failed to retrieve', year, 'events. Status code:', event_keys_response.status_code)
        continue
    
    # Convert the event keys json to a np array
    event_keys = np.array(event_keys_response.json())
    
    # List to store every alliance for that year
    year_alliances = []

    # for event_key in ['2002wa']:
    for event_key in event_keys:
        print(event_key)
        # Get the matches for that event
        match_response = requests.get('https://www.thebluealliance.com/api/v3/event/' + event_key + '/matches/simple', params={'X-TBA-Auth-Key': api_key})
        # Check request is valid
        if event_keys_response.status_code == 200:
            # Extract the red and blue team keys attributes from each match JSON object
            for match in match_response.json():
                # Check if the attribute exists before accessing it
                if 'alliances' in match and 'red' in match['alliances'] and 'team_keys' in match['alliances']['red']:
                    # get the numbers from the team keys
                    team_numbers = [int(''.join(filter(str.isdigit, team_key))) for team_key in match['alliances']['red']['team_keys']]
                    # append alliance number sum, color, match number, and event name
                    alliance_stats = [team_numbers, sum(team_numbers), 'red', match['comp_level']+str(match['match_number']), event_key]
                    # add the alliance to the year's alliances
                    year_alliances.append(alliance_stats)
                elif 'alliances' in match and 'blue' in match['alliances'] and 'team_keys' in match['alliances']['blue']:
                    # get the numbers from the team keys
                    team_numbers = [int(''.join(filter(str.isdigit, team_key))) for team_key in match['alliances']['blue']['team_keys']]
                    # append alliance number sum, color, match number, and event name
                    alliance_stats[team_numbers, sum(team_numbers), 'blue', match['comp_level']+str(match['match_number']), event_key]
                    # add the alliance to the year's alliances
                    year_alliances.append(alliance_stats)
        else:
            print('Failed to retrieve', event_key, 'events. Status code:', event_keys_response.status_code)
            continue
    # Sort the alliances by sum
    sorted_year_alliances = sorted(year_alliances, key=lambda x: x[1], reverse=True)
    # Print the first 5 elements using list slicing
    print('Highest 5 alliances in',year, ':', sorted_year_alliances[:5])
    # Print the last 5 elements using list slicing
    print('Lowest 5 alliances in', year, ':', sorted_year_alliances[-5:])