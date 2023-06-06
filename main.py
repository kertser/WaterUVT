from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import WaterCalculator

A_Lignin = 0.0072
B_Lignin = -2.1
C_Lignin = 138

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="htmldirectory")
filename = "UVT_output.csv"
defaultUVT = 65


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, waterUVT=defaultUVT):
    WaterCalculator.getWaterVector(waterUVT)

    Lignin = round(A_Lignin*waterUVT**2+B_Lignin*waterUVT+C_Lignin)
    # print(Save_to_CSV)
    return templates.TemplateResponse("home.html", {"request": request, "waterUVT": waterUVT, "Lignin": Lignin})


# RUN: uvicorn main:app --reload
@app.post("/")
async def handle_UVT(request: Request, UVT: int = Form(defaultUVT), Save_to_CSV: str = Form('')):
    WaterCalculator.getWaterVector(UVT, True)
    Lignin = round(A_Lignin*UVT**2+B_Lignin*UVT+C_Lignin)
    if Save_to_CSV == 'Save to CSV file':
        return FileResponse(path=filename, filename=filename, media_type='text/csv')
    else:
        return templates.TemplateResponse('home.html',  {"request": request, "waterUVT": UVT, "Lignin": Lignin, "Save_to_CSV": Save_to_CSV})