from fastapi import APIRouter, Depends, HTTPException, Form
from app.schemas.auth_schema import Token
from app.api.controllers import auth_controller
from app.api.deps import get_current_admin_kabupaten_role, get_current_user
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register/user")
def register_user(
    nik: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    nama_lengkap: str = Form(...),
    alamat_domisili: str = Form(...),
    id_kecamatan: Optional[int] = Form(None),
    id_kabupaten: Optional[int] = Form(None)
):
    return auth_controller.register_user(
        nik=nik,
        email=email,
        password=password,
        nama_lengkap=nama_lengkap,
        alamat_domisili=alamat_domisili,
        id_kecamatan=id_kecamatan,
        id_kabupaten=id_kabupaten,
        role_id=1
    )

@router.post("/register/admin-kecamatan")
def register_admin_kecamatan(
    nik: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    nama_lengkap: str = Form(...),
    alamat_domisili: str = Form(...),
    id_kecamatan: Optional[int] = Form(None),
    id_kabupaten: Optional[int] = Form(None),
    current_user: dict = Depends(get_current_admin_kabupaten_role)
):
    return auth_controller.register_user(
        nik=nik,
        email=email,
        password=password,
        nama_lengkap=nama_lengkap,
        alamat_domisili=alamat_domisili,
        id_kecamatan=id_kecamatan,
        id_kabupaten=id_kabupaten,
        role_id=2
    )

@router.post("/register/admin-kabupaten")
def register_admin_kabupaten():
    raise HTTPException(status_code=403, detail="Pendaftaran Admin Kabupaten murni dari developer, pembuatan manual di database.")

@router.post("/login", response_model=Token)
def login(
    email: str = Form(...),
    password: str = Form(...)
):
    return auth_controller.login_user(email=email, password=password)

@router.get("/me")
def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id_user": current_user.get("id_user"),
        "email": current_user.get("email"),
        "nama_lengkap": current_user.get("nama_lengkap"),
        "alamat_domisili": current_user.get("alamat_domisili"),
        "id_role": current_user.get("id_role"),
        "id_kecamatan": current_user.get("id_kecamatan"),
        "id_kabupaten": current_user.get("id_kabupaten")
    }
