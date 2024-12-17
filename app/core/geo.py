"""
Модуль обработки файлов .geojson и работы с картой
"""

from dataclasses import dataclass, field
import folium
from folium import plugins


@dataclass
class Map:
    map: folium.Map = field(default_factory=folium.Map)
    geojson_layer: folium.FeatureGroup = folium.FeatureGroup(name="GeoJSON")

    def __post_init__(self) -> None:
        self.update()

    @property
    def folium_map(self) -> folium.Map:
        return self.map

    @property
    def html(self) -> str:
        return self.map._repr_html_()

    def update(self) -> None:
        self.map = folium.Map()
        self.geojson_layer = folium.FeatureGroup(name="GeoJSON")
        folium.TileLayer("CartoDB Positron").add_to(self.map)
        folium.TileLayer("openstreetmap", attr="OpenStreetMap contributors").add_to(
            self.map
        )
        draw = plugins.Draw(export=True)
        draw.add_to(self.map)
        self.geojson_layer.add_to(self.map)
        folium.LayerControl().add_to(self.map)

    def add_geodata(self, geojson_data: str, name: str = "default") -> None:
        self.update()
        folium.GeoJson(geojson_data).add_to(self.geojson_layer)
        # self.geojson_layer.add_child(name=name)

    def save_map(self, path: str, type_: str = "html") -> None:
        with open(path, mode="w") as file:
            match type_:
                case "html":
                    file.write(self.map._repr_html_())
                case _:
                    file.write(self.map._repr_html_())
