from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    nik: str
    email: str
    password: str
    nama_lengkap: str
    alamat_domisili: str
    id_kecamatan: Optional[int] = None
    id_kabupaten: Optional[int] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
