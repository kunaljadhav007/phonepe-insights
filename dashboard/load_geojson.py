# dashboard/load_geojson.py

import requests

url = 'https://github.com/pnraj/Projects/raw/master/Phonephe_Pulse/data/states_india.geojson'
with open('states_india.geojson', 'wb') as f:
    f.write(requests.get(url).content)


print(df['state'].unique())
print([feature["properties"]["ST_NM"] for feature in india_geojson["features"]])