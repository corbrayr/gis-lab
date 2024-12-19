from io import StringIO
from contextlib import asynccontextmanager
from typing import AsyncIterator

import geopandas as gpd  # type: ignore
from fastapi import FastAPI, Request, File, UploadFile, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.core.geo import Map
from app.core.search import SearchNominatim
from app.dependencies.geo import get_map, get_search
from app.exceptions import CoordinatesNotFound


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield


app = FastAPI(title="GIS Application", lifespan=lifespan)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/ping")
async def ping():
    return "ok"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, map_: Map = Depends(get_map)):
    map_html = map_.html

    return templates.TemplateResponse(
        "index.html", {"request": request, "map_html": map_html}
    )


@app.post("/upload_geojson", response_class=HTMLResponse)
async def upload_geojson(
    request: Request,
    geojson_file: UploadFile = File(...),
    map_: Map = Depends(get_map),
):
    geojson_data = await geojson_file.read()
    gdf = gpd.read_file(StringIO(geojson_data.decode("utf-8")))
    map_.add_geodata(gdf)
    map_html = map_.html

    return templates.TemplateResponse(
        "index.html", {"request": request, "map_html": map_html}
    )


@app.post("/search_geo", response_class=HTMLResponse)
async def search_geo(
    request: Request,
    user_query: str = Form(...),
    map_: Map = Depends(get_map),
    search: SearchNominatim = Depends(get_search),
):
    try:
        coordinates = search.get_coordinates(user_query)
    except CoordinatesNotFound:
        print("Coordinates not found!")
    else:
        map_.add_marker(coordinates, user_query)
    finally:
        map_html = map_.html

    return templates.TemplateResponse(
        "index.html", {"request": request, "map_html": map_html}
    )
