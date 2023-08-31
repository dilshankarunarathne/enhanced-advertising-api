from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Image(BaseModel):
    image: str

@app.post("/evaluate_image")
async def evaluate_image(image: Image):
    age, gender = (23, 'M') # TODO: Replace with actual model
    return {"age": age, "gender": gender}
