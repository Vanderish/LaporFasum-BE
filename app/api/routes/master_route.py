from fastapi import APIRouter, Depends, Query
from app.schemas.master_schema import FasilitasUmumQuery, RuteResponse
from app.api.controllers import master_controller
from app.api.deps import get_current_user

router = APIRouter(prefix="/master", tags=["Master Data & Referensi"])

@router.get("/kecamatan")
def get_kecamatan(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_all_kecamatan(page, limit)

@router.get("/kategori")
def get_kategori(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_all_kategori(page, limit)

@router.get("/kategori/{id_kategori}")
def get_kategori_by_id(id_kategori: int, current_user: dict = Depends(get_current_user)):
    return master_controller.get_kategori_by_id(id_kategori)

@router.get("/fasilitas-umum")
def get_fasilitas_umum(
    nama: str = Query(None, description="Nama fasilitas untuk pencarian"),
    kategori: int = Query(None, description="ID kategori untuk filter"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_fasilitas_umum(nama=nama, kategori=kategori, page=page, limit=limit)

@router.get("/fasilitas-umum/{id_fasilitas}/rute")
def get_rute_fasilitas(id_fasilitas: int, current_user: dict = Depends(get_current_user)):
    return master_controller.get_rute_fasilitas(id_fasilitas)