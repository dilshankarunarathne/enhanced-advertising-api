from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

class Image(BaseModel):
    image: str

@app.post("/image")
async def evaluate_image(image: Image):
    age, gender = (23, 'M') # TODO: Replace with actual model
    return {"age": age, "gender": gender}


@app.websocket("/video")
async def video(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        # TODO: Process video data
        return {"age": 23, "gender": 'M'} # TODO: Replace with actual data
