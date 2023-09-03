from fastapi import APIRouter

router = APIRouter(
    prefix="/api/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async 
