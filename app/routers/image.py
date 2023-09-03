from fastapi import APIRouter

router = APIRouter(
    prefix="/api/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/login")

@router.post("/")
async def evaluate_image(image: UploadFile = File(...)):
