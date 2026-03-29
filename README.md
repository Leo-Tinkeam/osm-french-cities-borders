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