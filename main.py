from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import cv2
import numpy as np

app = FastAPI()


class Image(BaseModel):
    image: str


def process_video_data(data):
    frame_list = []

    # Create a VideoCapture object to read the MJPEG video data
    cap = cv2.VideoCapture()
    cap.open(cv2.CAP_MJPEG)
    cap.set(1, 0)  # Set the frame position to the beginning

    # Read the MJPEG video data as frames
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Resize the frame to your desired dimensions
        frame = cv2.resize(frame, (480, 360))  # Replace with your desired size

        # Preprocess the frame (e.g., normalize pixel values)
        frame = frame / 255.0  # Normalize pixel values to the range [0, 1]

        # Add the preprocessed frame to the list
        frame_list.append(frame)

    # Close the VideoCapture object
    cap.release()

    # Convert the list of frames to a NumPy array
    frames = np.array(frame_list)

    return frames


@app.post("/image")
async def evaluate_image(image: Image):
    age, gender = (23, 'M')  # TODO: Replace with actual model
    return {"age": age, "gender": gender}


@app.websocket("/video")
async def video(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()

        # Process the data to extract frames and preprocess them
        frames = process_video_data(data)

        # TODO: Send the frames to the model for evaluation

        # TODO: For testing, visualize the frames
        for frame in frames:

        return {"age": 23, "gender": 'M'}  # TODO: Replace with actual data
