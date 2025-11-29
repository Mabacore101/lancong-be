from fastapi import APIRouter
from services.package_service import get_packages, get_package_places

router = APIRouter(prefix="/packages", tags=["Packages"])

@router.get("/")
def list_packages():
    return get_packages()

@router.get("/{package_id}/places")
def package_places(package_id: int):
    return get_package_places(package_id)
