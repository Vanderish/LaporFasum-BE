from fastapi import HTTPException, UploadFile
from app.core.database import get_db_connection
from app.core.security import get_password_hash, verify_password
from typing import Optional
import cloudinary.uploader

DICEBEAR_URL = "https://api.dicebear.com/7.x/avataaars/svg?seed={}"

def get_user_profile(current_user: dict) -> dict:
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
    
    cursor = db.cursor(dictionary=True)
    
    try:
        id_user = current_user.get("id_user")
        
        cursor.execute("SELECT id_user, nama_lengkap, email, alamat_domisili, foto_profile FROM users WHERE id_user = %s", (id_user,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        if not user.get("foto_profile"):
            user["foto_profile"] = DICEBEAR_URL.format(user["email"])
        
        return {
            "id_user": user["id_user"],
            "nama_lengkap": user["nama_lengkap"],
            "email": user["email"],
            "alamat_domisili": user["alamat_domisili"],
            "foto_profile": user["foto_profile"]
        }
    finally:
        cursor.close()
        db.close()

def update_profile(
    current_user: dict,
    nama_lengkap: Optional[str] = None,
    alamat_domisili: Optional[str] = None
):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        id_user = current_user.get("id_user")
        
        cursor.execute("SELECT id_user FROM users WHERE id_user = %s", (id_user,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        update_fields = []
        params = []
        
        if nama_lengkap:
            update_fields.append("nama_lengkap = %s")
            params.append(nama_lengkap)
        
        if alamat_domisili:
            update_fields.append("alamat_domisili = %s")
            params.append(alamat_domisili)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diupdate")
        
        params.append(id_user)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id_user = %s"
        cursor.execute(query, tuple(params))
        db.commit()
        
        return get_user_profile(current_user)
    finally:
        cursor.close()
        db.close()

def update_foto_profile(current_user: dict, foto_profile: Optional[UploadFile] = None):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
    
    # Validate file if provided
    if foto_profile:
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]
        if foto_profile.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Format file tidak didukung. Gunakan JPG, PNG, WEBP, atau HEIC")
        
        # Upload ke Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                foto_profile.file,
                folder="profile_photos",
                timeout=60,
                resource_type="image",
                format="jpg",
                quality="auto:good"
            )
            foto_url = upload_result.get("secure_url")
            
            if not foto_url:
                raise HTTPException(status_code=500, detail="Gagal upload foto ke Cloudinary")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error upload Cloudinary: {str(e)}")
    else:
        foto_url = None  # Clear photo - will fallback to DiceBear
    
    cursor = db.cursor(dictionary=True)
    
    try:
        id_user = current_user.get("id_user")
        
        cursor.execute("SELECT id_user FROM users WHERE id_user = %s", (id_user,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        cursor.execute("UPDATE users SET foto_profile = %s WHERE id_user = %s", (foto_url, id_user))
        db.commit()
        
        return get_user_profile(current_user)
    finally:
        cursor.close()
        db.close()

def update_password(
    current_user: dict,
    password_lama: str,
    password_baru: str
):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        id_user = current_user.get("id_user")
        
        cursor.execute("SELECT password FROM users WHERE id_user = %s", (id_user,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        if not verify_password(password_lama, user["password"]):
            raise HTTPException(status_code=400, detail="Password lama tidak sesuai")
        
        password_hash = get_password_hash(password_baru)
        
        cursor.execute("UPDATE users SET password = %s WHERE id_user = %s", (password_hash, id_user))
        db.commit()
        
        return {"message": "Password berhasil diperbarui"}
    finally:
        cursor.close()
        db.close()