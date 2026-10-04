from fastapi import HTTPException, status, UploadFile
from app.core.security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_DAYS
from datetime import timedelta
from app.core.database import get_db_connection
from typing import Optional
import cloudinary
import cloudinary.uploader

async def register_user(
    nik: str,
    email: str,
    password: str,
    nama_lengkap: str,
    alamat_domisili: str,
    role_id: int,
    id_kecamatan: Optional[int] = None,
    id_kabupaten: Optional[int] = None,
    foto_ktp: Optional[UploadFile] = None,
    foto_profil: Optional[UploadFile] = None
):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id_user FROM users WHERE email = %s OR nik = %s", (email, nik))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email atau NIK sudah terdaftar"
            )
        
        hashed_password = get_password_hash(password)
        
        cursor.execute(
            "INSERT INTO users (nama_lengkap, nik, email, password, alamat_domisili, id_role, id_kecamatan, id_kabupaten) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nama_lengkap, nik, email, hashed_password, alamat_domisili, role_id, id_kecamatan, id_kabupaten)
        )
        db.commit()
    finally:
        cursor.close()
        db.close()
    
    return {"message": "User berhasil registrasi"}

def login_user(identifier: str, password: str):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id_user, email, password, nama_lengkap, alamat_domisili, id_role, id_kecamatan, id_kabupaten FROM users WHERE email = %s OR nik = %s", (identifier, identifier))
        user_dict = cursor.fetchone()
    finally:
        cursor.close()
        db.close()
    
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kredensial tidak valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(password, user_dict["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kredensial tidak valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={
            "id_user": user_dict["id_user"],
            "email": user_dict["email"],
            "nama_lengkap": user_dict["nama_lengkap"],
            "alamat_domisili": user_dict["alamat_domisili"],
            "id_role": user_dict["id_role"],
            "id_kecamatan": user_dict["id_kecamatan"],
            "id_kabupaten": user_dict["id_kabupaten"]
        }, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

def get_kecamatan_list():
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
    
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan ORDER BY nama_kecamatan")
        kecamatan_list = cursor.fetchall()
    finally:
        cursor.close()
        db.close()
    
    return kecamatan_list
