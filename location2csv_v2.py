######################################
# Extract geolocation information from the filewave server from a known inventory query. 
# Use the JSON response from your inventory query and reformat in a timestamped CSV file
# v 0.1
# Dave Herder
######################################

import requests, pprint, json, csv, time, os

url = 'https://<server>:20443//inv/api/v1/query_result_extended/<queryID>'
auth_token = '<authtoken>'
header = {'Authorization': auth_token, 'Content-Type': 'application/json'}

response = requests.get(url, headers=header)
data = response.json()

with open('location.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, sort_keys=True)

#trim JSON to make it parsable
lines = open('location.json').readlines()
open('location_trimmed.json', 'w').writelines(lines[5:-3])

#get time
current_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
output_name = 'location_%s.csv' % current_time

#convert JSON to csv
x = open('location_trimmed.json')
rows = json.load(x)
with open(output_name, 'wb+') as f:
    dict_writer = csv.DictWriter(f, fieldnames=['Client_device_name','Client_last_check_in','GeoLocation_longitude','GeoLocation_latitude','GeoLocation_horizontal_accuracy','GeoLocation_altitude','GeoLocation_altitude_accuracy','GeoLocation_location_date','GeoLocation_speed','GeoLocation_course'])
    dict_writer.writeheader()
    dict_writer.writerow(rows)
    
os.remove("location_trimmed.json")
os.remove("location.json")
