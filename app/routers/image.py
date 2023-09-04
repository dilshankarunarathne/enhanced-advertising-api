from fastapi import APIRouter, UploadFile, File, Depends

from app.security.authorize import get_current_user, credentials_exception, oauth2_scheme

"""
    routers for image evaluation
"""

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
        raise credentials_exception

    contents = await image.read()

    # TODO: send image to model for evaluation
    with open("D:/image.jpg", "wb") as f:
        f.write(contents)

    age = 23  # TODO: get age from model
    gender = 'Male'  # TODO: get gender from model

    return "{age: ", age, ", gender: ", gender, "}"  # TODO: return ad data as well
