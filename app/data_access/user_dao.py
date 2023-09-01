router = APIRouter(
    prefix="/auth",
    tags=["mockAuth"],
    responses={404: {"description": "Not found"}},
)