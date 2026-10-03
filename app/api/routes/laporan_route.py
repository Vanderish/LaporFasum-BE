from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from app.schemas.laporan_schema import LaporanCreate, LaporanUpdateStatus, LaporanResponse, RiwayatStatusResponse
from app.api.controllers import laporan_controller
from app.api.deps import get_current_user, get_current_admin_role
from typing import Optional

router = APIRouter(prefix="/laporan", tags=["Laporan & Tracking"])

@router.post("", response_model=dict)
def create_laporan(
    judul_laporan: str = Form(...),
    deskripsi: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    id_kategori: int = Form(...),
    id_kecamatan_kejadian: int = Form(None),
    foto_bukti: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    return laporan_controller.create_laporan(
        judul_laporan=judul_laporan,
        deskripsi=deskripsi,
        latitude=latitude,
        longitude=longitude,
        id_kategori=id_kategori,
        id_kecamatan_kejadian=id_kecamatan_kejadian,
        foto_bukti=foto_bukti,
        current_user=current_user
    )

@router.get("")
def get_laporan_list(
    status: Optional[str] = Query(None, description="Filter by status"),
    kategori: Optional[int] = Query(None, description="Filter by kategori"),
    search: Optional[str] = Query(None, description="Search by judul/deskripsi"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return laporan_controller.get_laporan_list(
        current_user=current_user,
        status=status,
        kategori=kategori,
        search=search,
        page=page,
        limit=limit
    )

@router.get("/saya")
def get_laporan_saya(current_user: dict = Depends(get_current_user)):
    return laporan_controller.get_laporan_saya(current_user)

@router.get("/{id_laporan}")
def get_laporan_by_id(id_laporan: int, current_user: dict = Depends(get_current_user)):
    return laporan_controller.get_laporan_by_id(id_laporan, current_user)

@router.put("/{id_laporan}/status")
def update_laporan_status(
    id_laporan: int,
    status_terkini: str = Form(...),
    kewenangan_penanganan: str = Form(...),
    tanggapan_admin: str = Form(None),
    current_user: dict = Depends(get_current_admin_role)
):
    return laporan_controller.update_laporan_status(
        id_laporan=id_laporan,
        status_terkini=status_terkini,
        kewenangan_penanganan=kewenangan_penanganan,
        tanggapan_admin=tanggapan_admin,
        current_user=current_user
    )

@router.delete("/{id_laporan}")
def delete_laporan(id_laporan: int, current_user: dict = Depends(get_current_user)):
    return laporan_controller.delete_laporan(id_laporan, current_user)

@router.get("/{id_laporan}/riwayat")
def get_riwayat_laporan(id_laporan: int, current_user: dict = Depends(get_current_user)):
    return laporan_controller.get_riwayat_laporan(id_laporan, current_user)