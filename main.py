from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Image(BaseModel):
    image: str

@app.post("/evaluate_image")
async def evaluate_image(image: Image):
    # Call the method that evaluates the image and returns the age and gender of the user
    age, gender = evaluate(image.image)
    return {"age": age, "gender": gender}
