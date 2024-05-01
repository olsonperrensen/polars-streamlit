from fastapi import APIRouter

router = APIRouter()

@router.get("/data_types")
def get_data_types():
    return ["Preprocessed EEG Data", "Raw EEG Data"]