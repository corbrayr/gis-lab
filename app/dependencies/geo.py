from app.core.geo import Map

map_instance = Map()


def get_map() -> Map:
    return map_instance
