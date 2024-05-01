from fastapi import APIRouter

router = APIRouter()

@router.get("/patients")
def get_patients():
    ids = [f"{i:04d}" for i in range(44)]
    return ids