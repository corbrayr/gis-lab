"""
Модуль обработки поиска местоположения
"""

from typing import NamedTuple
from functools import partial
from dataclasses import dataclass, field
from geopy.geocoders import Nominatim
from app.exceptions import CoordinatesNotFound


class Coordinates(NamedTuple):
    lat: float
    lon: float


@dataclass
class SearchNominatim:
    geolocator: Nominatim = field(
        default_factory=partial(Nominatim, user_agent="geo-service")
    )

    def get_coordinates(self, query: str) -> Coordinates:
        location = self.geolocator.geocode(query)
        if location:
            return Coordinates(lat=location.latitude, lon=location.longitude)
        raise CoordinatesNotFound


if __name__ == "__main__":
    search = SearchNominatim()
    query = "Berlin"
    print(search.get_coordinates(query))
