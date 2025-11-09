from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# تفعيل CORS للسماح للـ HTML بالتواصل مع الـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تقديم الملفات الثابتة (static) مثل index.html و CSS و JS
app.mount("/static", StaticFiles(directory="static"), name="static")

class BMIOutput(BaseModel):
    bmi: float
    message: str

@app.get("/")
def serve_index():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/calculate_bmi")
def calculate_bmi(
    w: float = Query(..., gt=20, lt=200, description="Weight in kg"),
    h: float = Query(..., gt=1, lt=2.5, description="Height in m")
):
    bmi = float(w) / (float(h) ** 2)

    if bmi < 18.5:
        message = 'لديك نقص في الوزن'
    elif 18.5 <= bmi < 25:
        message = 'لديك وزن طبيعي'
    elif 25 <= bmi < 30:
        message = 'لديك زيادة في الوزن'
    else:
        message = 'انت تعاني من السمنة'

    return BMIOutput(bmi=bmi, message=message)

