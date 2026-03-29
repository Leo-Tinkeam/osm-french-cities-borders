from database.ttypes import Point, Shape, Border as BorderThrift, DictNameToBorder, DictNameToCenter
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from shapely import ops, geometry
from generate_france_dict import City, Border, WayDescriptor, dict_file_name
import pickle

def parse_border(liste_ref_role: Border):
    outer_coords: list[Shape] = []
    inner_coords_list: list[Shape] = []
    for way_descriptor in liste_ref_role.related_objects:
        if way_descriptor.id not in ways:
            continue
        node_ids = ways[way_descriptor.id]
        shape = []
        for nid in node_ids:
            if nid in nodes:
                coord_tuple = nodes[nid]
                shape.append(Point(longitude=coord_tuple[0], lattitude=coord_tuple[1]))
        if len(shape) < 3: # Need at least 3 points to have a non-null area
            continue
        if way_descriptor.role == "outer":
            outer_coords.append(Shape(points=shape))
        elif way_descriptor.role == "inner":
            inner_coords_list.append(Shape(points=shape))

    return BorderThrift(outers=outer_coords, inners=inner_coords_list)

def get_center(border: BorderThrift):
    def parse_shape(shape: Shape):
        polygon = [(p.longitude, p.lattitude) for p in shape.points]
        return polygon
    def clean_poly(polygon_list, indice):
        if not polygon_list[indice].is_valid:
            polygon_list[indice] = polygon_list[indice].buffer(0)

    outer_polys = [geometry.Polygon(parse_shape(p)) for p in border.outers]
    inner_polys = [geometry.Polygon(parse_shape(p)) for p in border.inners]
    for i in range(len(outer_polys)):
        clean_poly(outer_polys, i)
    for i in range(len(inner_polys)):
        clean_poly(inner_polys, i)

    if len(outer_polys) == 0:
        return -1
    all_outers = ops.unary_union(outer_polys)
    if len(inner_polys) != 0:
        all_inners = ops.unary_union(inner_polys)
        final_shape = all_outers.difference(all_inners)
    else:
        final_shape = all_outers

    centroid = final_shape.centroid
    return Point(
        longitude=centroid.x,
        lattitude=centroid.y
    )

if __name__=="__main__":
    with open(dict_file_name, 'rb') as f:
        france_dict: dict[str] = pickle.load(f)

    old_cities: dict[int, City] = france_dict["cities"]
    ways: dict[int, list[int]] = france_dict["ways"]
    nodes: dict[int, tuple[float, float]] = france_dict["nodes"]

    name_to_border_dict = {}
    name_to_center_dict = {}
    for key, value in old_cities.items():
        border = parse_border(value.border)
        center = get_center(border)
        if center == -1:
            continue
        name_to_border_dict[value.name] = border
        name_to_center_dict[value.name] = center
    
    name_to_border = DictNameToBorder(name_to_border_dict)
    name_to_center = DictNameToCenter(name_to_center_dict)

    transport_out = TTransport.TMemoryBuffer()
    protocol_out = TBinaryProtocol.TBinaryProtocol(transport_out)
    name_to_border.write(protocol_out)
    payload = transport_out.getvalue()
    with open("name_to_border.bin", "wb") as f:
        f.write(payload)

    transport_out = TTransport.TMemoryBuffer()
    protocol_out = TBinaryProtocol.TBinaryProtocol(transport_out)
    name_to_center.write(protocol_out)
    payload = transport_out.getvalue()
    with open("name_to_center.bin", "wb") as f:
        f.write(payload)