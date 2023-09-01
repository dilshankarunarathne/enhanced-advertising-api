router = APIRouter(
    prefix="/mockAuth",
    tags=["mockAuth"],
    responses={404: {"description": "Not found"}},
)