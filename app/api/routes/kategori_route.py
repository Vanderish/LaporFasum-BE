from fastapi import APIRouter, Depends, Query
from app.api.controllers import kategori_controller
from app.api.deps import get_current_user

router = APIRouter(prefix="/kategori", tags=["Kategori Fasilitas"])

@router.get("/{id_kategori}")
def get_kategori_by_id(id_kategori: int, current_user: dict = Depends(get_current_user)):
    return kategori_controller.get_kategori_by_id(id_kategori)
