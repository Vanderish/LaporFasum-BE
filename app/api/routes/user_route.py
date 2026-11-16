from fastapi import APIRouter, Depends, Form
from app.api.controllers import user_controller
from app.api.deps import get_current_user
from typing import Optional

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return user_controller.get_user_profile(current_user)

@router.put("/profile")
def update_profile(
    nama_lengkap: Optional[str] = Form(None),
    alamat_domisili: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    return user_controller.update_profile(
        current_user=current_user,
        nama_lengkap=nama_lengkap,
        alamat_domisili=alamat_domisili
    )

@router.put("/profile/foto")
def update_foto_profile(
    foto_profile: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    return user_controller.update_foto_profile(
        current_user=current_user,
        foto_profile=foto_profile
    )

@router.put("/profile/password")
def update_password(
    password_lama: str = Form(...),
    password_baru: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    return user_controller.update_password(
        current_user=current_user,
        password_lama=password_lama,
        password_baru=password_baru
    )