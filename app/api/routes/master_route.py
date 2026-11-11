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

@router.get("/notifikasi")
def get_notifikasi(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_notifikasi(current_user, page, limit)

@router.get("/jalan/nasional")
def get_jalan_nasional(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_nasional(page, limit)

@router.get("/jalan/provinsi")
def get_jalan_provinsi(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_provinsi(page, limit)

@router.get("/jalan/kecamatan")
def get_jalan_kecamatan(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kecamatan(page, limit)

@router.get("/jalan/kabupaten")
def get_jalan_kabupaten(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kabupaten(page, limit)

@router.get("/jalan/arteri-primer")
def get_jalan_arteri_primer(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_arteri_primer(page, limit)

@router.get("/jalan/kolektor-primer-1")
def get_jalan_kolektor_primer_1(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kolektor_primer_1(page, limit)

@router.get("/jalan/kolektor-primer-2")
def get_jalan_kolektor_primer_2(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kolektor_primer_2(page, limit)

@router.get("/jalan/kolektor-primer-3")
def get_jalan_kolektor_primer_3(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kolektor_primer_3(page, limit)

@router.get("/jalan/arteri-sekunder")
def get_jalan_arteri_sekunder(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_arteri_sekunder(page, limit)

@router.get("/jalan/kolektor-primer-4")
def get_jalan_kolektor_primer_4(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kolektor_primer_4(page, limit)

@router.get("/jalan/kolektor-sekunder")
def get_jalan_kolektor_sekunder(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_kolektor_sekunder(page, limit)

@router.get("/jalan/lingkungan-primer")
def get_jalan_lingkungan_primer(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_lingkungan_primer(page, limit)

@router.get("/jalan/lingkungan-sekunder")
def get_jalan_lingkungan_sekunder(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_lingkungan_sekunder(page, limit)

@router.get("/jalan/lokal-primer")
def get_jalan_lokal_primer(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_lokal_primer(page, limit)

@router.get("/jalan/lokal-sekunder")
def get_jalan_lokal_sekunder(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    return master_controller.get_jalan_lokal_sekunder(page, limit)