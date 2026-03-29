This project aims to generate two dictionaries:
- `name_to_border` that give the border of a city (that can be displayed over OSM tiles)
- `name_to_center` that can be use as a list of city and also gives geometric center of cities

Everything is done for France only but I think that you can use it for an other country by using another endpoint on `download_france_binary.py`
I plan run this process monthly for France on a private server. If you are working on an open-source project and want to access these results via my API directly, avoiding the need to run the full pipeline yourself, feel free to contact me at leosarcy@tinkeam.fr to discuss access.

# Generate code (for auto-completion)

## Install Thrift

> sudo apt install thrift-compiler

## Generate python code

> thrift -gen py -out . database.thrift

# Download data from geofabrick (restriction of https://planet.openstreetmap.org/ for France)

> uv run download_france_binary.py

# Generate intermediate file that contains data that can be read faster for our objective

> uv run generate_france_dict.py

# Get final binaries (see "Generate code" before)

> uv run generate_france_databases.py