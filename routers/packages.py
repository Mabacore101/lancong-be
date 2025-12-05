from fastapi import APIRouter, HTTPException
from services.package_service import get_package, get_packages

router = APIRouter(prefix="/packages", tags=["Packages"])


@router.get("/{package_id}")
def package_detail(package_id: int):
    package = get_package(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


@router.get("")
def list_packages(limit: int = 10):
    return get_packages(limit)
