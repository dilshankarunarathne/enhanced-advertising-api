from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Image(BaseModel):
    image: str

@app.post("/evaluate_image")
async def evaluate_image(image: Image):
    age, gender = (23, 'M')
    return {"age": age, "gender": gender}
