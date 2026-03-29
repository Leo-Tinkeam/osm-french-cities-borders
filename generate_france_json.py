import pickle
from pydantic import BaseModel
from generate_france_dict import City, Border, WayDescriptor, dict_file_name

class ShapeDesc(BaseModel):
    points: list[tuple[float, float]]

class BorderDesc(BaseModel):
    outers: list[ShapeDesc]
    inners: list[ShapeDesc]

class CityDesc(BaseModel):
    osm_id: int
    name: str
    border: BorderDesc

class Database(BaseModel):
    cities: list[CityDesc]

def parse_border(liste_ref_role: Border):
    outer_coords: list[ShapeDesc] = []
    inner_coords_list: list[ShapeDesc] = []
    for way_descriptor in liste_ref_role.related_objects:
        if way_descriptor.id not in ways:
            continue
        node_ids = ways[way_descriptor.id]
        shape = []
        for nid in node_ids:
            if nid in nodes:
                shape.append(nodes[nid])
        if len(shape) < 3: # Need at least 3 points to have a non-null area
            continue
        if way_descriptor.role == "outer":
            outer_coords.append(ShapeDesc(points=shape))
        elif way_descriptor.role == "inner":
            inner_coords_list.append(ShapeDesc(points=shape))

    return BorderDesc(outers=outer_coords, inners=inner_coords_list)

if __name__=="__main__":
    with open(dict_file_name, 'rb') as f:
        france_dict: dict[str] = pickle.load(f)

    old_cities: dict[int, City] = france_dict["cities"]
    ways: dict[int, list[int]] = france_dict["ways"]
    nodes: dict[int, tuple[float, float]] = france_dict["nodes"]

    new_cities = []
    for key, value in old_cities.items():
        border = parse_border(value.border)
        city = CityDesc(osm_id=key, name=value.name, border=border)
        new_cities.append(city)
    
    database = Database(cities=new_cities)
    database_json = database.model_dump_json(indent=2)

    with open("french_cities.json", "w", encoding="utf-8") as f:
        f.write(database_json)