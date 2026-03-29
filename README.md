# Download data from geofabrick (restriction of https://planet.openstreetmap.org/ for France)

> uv run download_france_binary.py

# Generate intermediate file that contains data that can be read faster for our objective

> uv run generate_france_dict.py

# Get final json

> uv run generate_france_json.py