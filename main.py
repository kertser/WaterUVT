from fastapi import FastAPI, Body, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import WaterCalculator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="htmldirectory")

@app.get("/", response_class = HTMLResponse)
def main(request: Request):
    waterUVT = 55#[%-1cm]
    WaterCalculator.getWaterVector(waterUVT)
    return templates.TemplateResponse("home.html", {"request": request, "waterUVT": waterUVT})

    #WaterUVT = 55#[%-1cm]
    #WaterCalculator.getWaterVector(WaterUVT)



