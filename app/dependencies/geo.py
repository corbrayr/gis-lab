from app.core.geo import Map
from app.core.search import SearchNominatim

map_instance = Map()
search_instance = SearchNominatim()


def get_map() -> Map:
    return map_instance


def get_search() -> SearchNominatim:
    return search_instance
