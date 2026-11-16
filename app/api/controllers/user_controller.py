from fastapi import HTTPException
from app.core.database import get_db_connection
from app.core.security import get_password_hash, verify_password
from typing import Optional

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
        
        # Fallback ke DiceBear jika foto_profile null/kosong
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
    alamat_domisili: Optional[str] = None,
    foto_profile: Optional[str] = None,
    password_lama: Optional[str] = None,
    password_baru: Optional[str] = None
):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        id_user = current_user.get("id_user")
        
        cursor.execute("SELECT password, foto_profile FROM users WHERE id_user = %s", (id_user,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
        if password_baru:
            if not password_lama:
                raise HTTPException(status_code=400, detail="Password lama harus diisi")
            
            if not verify_password(password_lama, user["password"]):
                raise HTTPException(status_code=400, detail="Password lama tidak sesuai")
            
            password_hash = get_password_hash(password_baru)
        else:
            password_hash = None
        
        update_fields = []
        params = []
        
        if nama_lengkap:
            update_fields.append("nama_lengkap = %s")
            params.append(nama_lengkap)
        
        if alamat_domisili:
            update_fields.append("alamat_domisili = %s")
            params.append(alamat_domisili)
        
        if foto_profile is not None:
            update_fields.append("foto_profile = %s")
            params.append(foto_profile)
        
        if password_hash:
            update_fields.append("password = %s")
            params.append(password_hash)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diupdate")
        
        params.append(id_user)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id_user = %s"
        cursor.execute(query, tuple(params))
        db.commit()
        
        # Return updated profile
        return get_user_profile(current_user)
    finally:
        cursor.close()
        db.close()
