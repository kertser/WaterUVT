from fastapi import FastAPI, Body, Request, Form
#from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import WaterCalculator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="htmldirectory")

@app.get("/", response_class = HTMLResponse)
async def main(request: Request, waterUVT = 55):
    #waterUVT = 55#[%-1cm]
    WaterCalculator.getWaterVector(waterUVT)
    return templates.TemplateResponse("home.html", {"request": request, "waterUVT": waterUVT})

@app.post("/")
async def handle_UVT(request: Request, UVT: int = Form(...)):
    return templates.TemplateResponse('home.html',  {"request": request, "waterUVT": UVT})




