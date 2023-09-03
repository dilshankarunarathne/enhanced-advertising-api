from fastapi import APIRouter, UploadFile, File, Depends

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
    if image.content_type != "image/jpeg":
        return "Only jpeg images are supported"

    if get_current_user(token) is None:
        return "Invalid token"
    contents = await image.read()
    with open("D:/image.jpg", "wb") as f:
        f.write(contents)

    return "Image received"
