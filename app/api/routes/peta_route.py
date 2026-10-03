from fastapi import APIRouter, Depends, Query
from app.schemas.peta_schema import InfrastrukturFilter
from app.api.controllers import peta_controller
from app.api.deps import get_current_user

router = APIRouter(prefix="/peta", tags=["Peta & Visualisasi"])

@router.get("/batas-wilayah")
def get_batas_wilayah(current_user: dict = Depends(get_current_user)):
    return peta_controller.get_batas_wilayah()

@router.get("/infrastruktur")
def get_infrastruktur(
    kepemilikan: str = Query(None, description="Filter by kepemilikan: Desa, Kecamatan, Kabupaten, Provinsi, Nasional"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=200, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return peta_controller.get_infrastruktur(kepemilikan=kepemilikan, page=page, limit=limit)

@router.get("/titik-laporan")
def get_titik_laporan(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=200, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return peta_controller.get_titik_laporan(page=page, limit=limit)