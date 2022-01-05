from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import WaterCalculator

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class = HTMLResponse)
async def main():
    WaterUVT = 55#[%-1cm]
    WaterCalculator.getWaterVector(WaterUVT)
    content = head_html + """
    <marquee width="525" behavior="alternate"><h1 style="color:red;font-family:Arial">Please set your Water UVT254</h1></marquee>
    <br>
    <img src="static/UVTvsWavelength.png" alt="UVT of the Water">
    """
    return content

head_html = """
<head>
    <meta name = "viewport" content = "width=device-width, initial-scale=1"/>
</head>
<body style="background-color:powderblue;">
<center>
"""
