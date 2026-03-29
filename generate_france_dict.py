import osmium

binary_file_name = "france-latest.osm.pbf"
dict_file_name = "france_dict.pkl"

class City:
    def __init__(self, name: str, border):
        self.name: str = name
        self.border: Border = border

class Border:
    def __init__(self, related_ways):
        self.related_objects: list[WayDescriptor] = related_ways

class WayDescriptor:
    def __init__(self, id, role):
        self.id: int = id
        self.role: str = role

class CityHandler(osmium.SimpleHandler):
    def relation(self, r):
        tags = r.tags
        if (tags.get("type") == "boundary" and
            tags.get("boundary") == "administrative" and
            tags.get("admin_level") == "8"):
            
            border = Border([WayDescriptor(m.ref, m.role) for m in r.members])
            cities[r.id] = City(name=tags.get("name"), border=border)

class WayCollector(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def way(self, w):
        if w.id in way_id_needed:
            ways[w.id] = [n.ref for n in w.nodes]
            self.count += 1
            if self.count == 10000:
                print("Number of ways :", len(ways), "of", len(way_id_needed), "(predicted)")
                self.count = 0

class NodeCollector(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def node(self, n):
        if n.id in node_id_needed:
            nodes[n.id] = (n.location.lon, n.location.lat)
            self.count += 1
            if self.count == 100000:
                print("Number of nodes :", len(nodes), "of", len(node_id_needed))
                self.count = 0

if __name__ == "__main__":
    cities: dict[int, City] = {}
    ways = {}
    nodes = {}

    handler = CityHandler()
    handler.apply_file(binary_file_name)
    print("Number of cities :", len(cities))

    way_id_needed: set[int] = set()
    for key, value in cities.items():
        for way in value.border.related_objects:
            way_id_needed.add(way.id)
    print("Way_Id needed :", len(way_id_needed))

    handler = WayCollector()
    handler.apply_file(binary_file_name, locations=False)
    print("End of ways processing !", len(ways), "ways in total")

    node_id_needed = set()
    for key, value in ways.items():
        for id in value:
            node_id_needed.add(id)
    print("Node_Id needed :", len(node_id_needed))

    handler = NodeCollector()
    handler.apply_file(binary_file_name, locations=True)
    print("End of nods processing!", len(nodes), "nodes in total")

    import pickle
    france_dict = {"cities": cities, "ways": ways, "nodes": nodes}
    with open(dict_file_name, 'wb') as f:
        pickle.dump(france_dict, f)