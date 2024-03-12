import json, requests, time
import numpy as np
import os
from dotenv import load_dotenv

# Load API key environment variable from .env file
load_dotenv()
# Access API key
api_key = os.environ['API_KEY']

# Set up the output files with the correct headers
highestResults = open('highestResults.txt', 'w')
highestResults.write('|Year | Sum | Alliance | Event | Match | Color|\n|--- | --- | --- | --- | --- | ---|\n')
highestResults.close()
lowestResults = open('lowestResults.txt', 'w')
lowestResults.write('|Year | Sum | Alliance | Event | Match | Color|\n|--- | --- | --- | --- | --- | ---|\n')
lowestResults.close()

# Get every event with match data
for year in range(2002, 2025):
    start_time = time.time()
    # No matches in 2021
    if (year == 2021):
        continue
    
    # API call for event keys
    event_keys_response = requests.get('https://www.thebluealliance.com/api/v3/events/'+str(year), params={'X-TBA-Auth-Key': api_key})

    # Save this request for a year's events locally, as a json file.
    if event_keys_response.status_code == 200:
        data = event_keys_response.json()
        official_events = []
        for event in data:
            if (event['event_type'] < 99): # I genuinely have no idea what 'event_type' actually is, but alas this seems to work.
                official_events.append(event['key'])
                # print(event['key']+str(event['event_type']), 'event keys saved successfully.')
    else:
        print('Failed to retrieve', year, 'events. Status code:', event_keys_response.status_code)
        continue
    
    # Convert the event keys json to a np array
    event_keys = np.array(official_events)
    
    # List to store every alliance for that year
    year_alliances = []

    for event_key in event_keys:
        print('Tabulating:', event_key)
        # Get the matches for that event
        match_response = requests.get('https://www.thebluealliance.com/api/v3/event/' + event_key + '/matches/simple', params={'X-TBA-Auth-Key': api_key})
        # Check request is valid
        if event_keys_response.status_code == 200:
            # Extract the red and blue team keys attributes from each match JSON object
            for match in match_response.json():
                # Check if the attribute exists before accessing it
                if 'alliances' in match and 'red' in match['alliances'] and 'team_keys' in match['alliances']['red']:
                    # get the numbers from the team keys
                    team_numbers = [int(''.join(filter(str.isdigit, team_key))) for team_key in match['alliances']['red']['team_keys'] if int(''.join(filter(str.isdigit, team_key))) < 9980]
                    # if alliance is invalid, skip to the next alliance
                    if len(team_numbers) == 0 or len(team_numbers) != 3:
                        continue
                    # append alliance number sum, color, match number, and event name
                    alliance_stats = [team_numbers, sum(team_numbers), 'red', match['comp_level']+str(match['match_number']), event_key]
                    # add the alliance to the year's alliances
                    year_alliances.append(alliance_stats)
                if 'alliances' in match and 'blue' in match['alliances'] and 'team_keys' in match['alliances']['blue']:
                    # get the numbers from the team keys
                    team_numbers = [int(''.join(filter(str.isdigit, team_key))) for team_key in match['alliances']['blue']['team_keys'] if int(''.join(filter(str.isdigit, team_key))) <= 9980]
                    # if alliance is invalid, skip to the next alliance
                    if len(team_numbers) == 0 or len(team_numbers) != 3:
                        continue                   
                    # append alliance number sum, color, match number, and event name
                    alliance_stats = [team_numbers, sum(team_numbers), 'blue', match['comp_level']+str(match['match_number']), event_key]
                    # add the alliance to the year's alliances
                    year_alliances.append(alliance_stats)
        else:
            print('Failed to retrieve', event_key, 'events. Status code:', event_keys_response.status_code)
            continue
    # Sort the alliances by sum
    sorted_year_alliances = sorted(year_alliances, key=lambda x: x[1], reverse=True)
    # Open the results files
    highestResults = open('highestResults.txt', 'a')
    lowestResults = open('lowestResults.txt', 'a')
    if year != 2003:
        # Write content to the files
        highestResults.write('|'+str(year)+' | '+str(sorted_year_alliances[:1][0][1])+' | '+str(sorted_year_alliances[:1][0][0])+' | '+str(sorted_year_alliances[:1][0][4])+' | '+str(sorted_year_alliances[:1][0][3])+' | '+str(sorted_year_alliances[:1][0][2])+'|\n')
        lowestResults.write('|'+str(year)+' | '+str(sorted_year_alliances[-1:][0][1])+' | '+str(sorted_year_alliances[-1:][0][0])+' | '+str(sorted_year_alliances[-1:][0][4])+' | '+str(sorted_year_alliances[-1:][0][3])+' | '+str(sorted_year_alliances[-1:][0][2])+'|\n')
    # Close the text files
    highestResults.close()
    lowestResults.close()
    print(year, 'took ', time.time() - start_time, ' seconds to process.') # Message of shame