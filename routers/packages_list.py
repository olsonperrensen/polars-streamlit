from fastapi import APIRouter

router = APIRouter()


@router.get("/packages_list")
async def get_packages():
    requirements_file = "requirements.txt"
    with open(requirements_file, "r") as file:
        packages = file.read().splitlines()
    return packages
