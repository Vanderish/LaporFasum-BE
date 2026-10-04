from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from app.schemas.auth_schema import Token, UserRegister, UserLogin
from app.api.controllers import auth_controller
from app.api.deps import get_current_admin_kabupaten_role, get_current_user
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register/user")
async def register_user(user_data: UserRegister):
    return await auth_controller.register_user(
        nik=user_data.nik,
        email=user_data.email,
        password=user_data.password,
        nama_lengkap=user_data.nama_lengkap,
        alamat_domisili=user_data.alamat_domisili,
        id_kecamatan=user_data.id_kecamatan,
        id_kabupaten=user_data.id_kabupaten,
        role_id=1
    )

@router.post("/register/admin-kecamatan")
async def register_admin_kecamatan(
    nik: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    nama_lengkap: str = Form(...),
    alamat_domisili: str = Form(...),
    id_kecamatan: str = Form(...),
    id_kabupaten: Optional[str] = Form(None),
    foto_ktp: Optional[UploadFile] = File(None),
    foto_profil: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_admin_kabupaten_role)
):
    return await auth_controller.register_user(
        nik=nik,
        email=email,
        password=password,
        nama_lengkap=nama_lengkap,
        alamat_domisili=alamat_domisili,
        id_kecamatan=int(id_kecamatan) if id_kecamatan else None,
        id_kabupaten=int(id_kabupaten) if id_kabupaten else None,
        role_id=2,
        foto_ktp=foto_ktp,
        foto_profil=foto_profil
    )

@router.post("/register/admin-kabupaten")
def register_admin_kabupaten():
    raise HTTPException(status_code=403, detail="Pendaftaran Admin Kabupaten murni dari developer, pembuatan manual di database.")

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    return auth_controller.login_user(identifier=login_data.identifier, password=login_data.password)

@router.get("/kecamatan")
def get_kecamatan():
    return auth_controller.get_kecamatan_list()

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
