from fastapi import APIRouter, Depends, Form
from app.api.controllers import user_controller
from app.api.deps import get_current_user
from typing import Optional

router = APIRouter(prefix="/user", tags=["User"])

@router.put("/profile")
def update_profile(
    nama_lengkap: Optional[str] = Form(None),
    alamat_domisili: Optional[str] = Form(None),
    password_lama: Optional[str] = Form(None),
    password_baru: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    return user_controller.update_profile(
        current_user=current_user,
        nama_lengkap=nama_lengkap,
        alamat_domisili=alamat_domisili,
        password_lama=password_lama,
        password_baru=password_baru
    )
