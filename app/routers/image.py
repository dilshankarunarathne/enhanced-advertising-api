from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth import oauth2_scheme

router = APIRouter(
    prefix="/api/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)


@router.post("/evaluate")
async def evaluate_image(
        image: UploadFile = File(...),
        token: str = Depends(oauth2_scheme)
):
    contents = await image.read()
    with open("D:/image.jpg", "wb") as f:
        f.write(contents)

    return "Image received"
