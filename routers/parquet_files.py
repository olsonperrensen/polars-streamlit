import requests
from fastapi import APIRouter

router = APIRouter()


@router.get("/parquet_files")
def get_parquet_files(patient_id: str, data_type: str):
    r = requests.get(
        "https://datasets-server.huggingface.co/parquet?dataset=NOttheol/EEG-Talha-Alakus-Gonen-Turkoglu"
    )
    j = r.json()

    # Get all parquet files from the response
    all_files = j["parquet_files"]

    # Calculate the start and end indices for the patient's files
    patient_num = int(patient_id)
    start_index = patient_num * 5
    end_index = start_index + 5

    # Filter the files based on the patient's indices, split, and data type
    if data_type == "Preprocessed EEG Data":
        patient_files = [
            f
            for f in all_files
            if start_index <= int(f["filename"].split(".")[0]) < end_index
            and f["split"] == "train"
            and int(f["filename"].split(".")[0]) % 2 != 0
        ]
    elif data_type == "Raw EEG Data":
        patient_files = [
            f
            for f in all_files
            if start_index <= int(f["filename"].split(".")[0]) < end_index
            and f["split"] == "train"
            and int(f["filename"].split(".")[0]) % 2 == 0
        ]
    else:
        return {"error": "Invalid data type"}

    # Extract the URLs of the patient's files
    urls = [f["url"] for f in patient_files]

    return urls
