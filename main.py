from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import WaterCalculator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="htmldirectory")
filename = "UVT_output.csv"


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, waterUVT=65):
    WaterCalculator.getWaterVector(waterUVT)
    # print(Save_to_CSV)
    return templates.TemplateResponse("home.html", {"request": request, "waterUVT": waterUVT})


@app.post("/")
def handle_UVT(request: Request, UVT: int = Form(...), Save_to_CSV: bool = Form(False)):
    WaterCalculator.getWaterVector(UVT,True)
    if Save_to_CSV is True:
        FileResponse(path=filename, filename=filename, media_type='text/csv')
    return templates.TemplateResponse('home.html',  {"request": request, "waterUVT": UVT, "Save_to_CSV": Save_to_CSV})
