namespace py database

struct DictNameToBorder {
    1: map<string, Border> dict,
}

struct Border {
    1: list<Shape> outers,
    2: list<Shape> inners,
}

struct Shape {
    1: list<Point> points,
}

struct Point {
    1: double longitude,
    2: double lattitude,
}

struct DictNameToCenter {
    1: map<string, Point> dict,
}