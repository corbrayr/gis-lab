from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import folium


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield

app = FastAPI(
    title='GIS Application',
    lifespan=lifespan
)

@app.get('/ping')
async def ping():
    return 'ok'

@app.get('/')
async def main():
    # Создаем карту с центром в заданных координатах
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)  # Москва

    # Сохраняем карту в HTML файл
    map_html = "map.html"
    m.save(map_html)

    # Читаем содержимое HTML файла
    with open(map_html, "r", encoding="utf-8") as f:
        map_data = f.read()

    return HTMLResponse(content=map_data)