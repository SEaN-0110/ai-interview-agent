from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def home():
    return {"message": "AI Interview Agent Running"}
