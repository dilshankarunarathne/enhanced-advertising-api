import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, UploadFile, File
from pydantic import BaseModel
from starlette.responses import JSONResponse

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


# For captured images
@app.post("/image")
async def evaluate_image(image: UploadFile = File(...)):
    # Read the contents of the uploaded file
    contents = await image.read()

    # Save the image to a file
    with open("D:/image.jpg", "wb") as f:
        f.write(contents)

    return "Image received"


# For video streams
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
            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        return {"age": 23, "gender": 'M'}  # TODO: Replace with actual data


# For video file uploads
@app.post("/upload/")
async def upload_video(file: UploadFile):
    print("Upload endpoint invoked...")
    if file.content_type != "video/mp4":
        return JSONResponse(content={"message": "Invalid file format"}, status_code=400)

    video_data = await file.read()

    # Process the video_data as needed, e.g., save it to a file or perform analysis

    return JSONResponse(content={"message": "Video uploaded successfully"})