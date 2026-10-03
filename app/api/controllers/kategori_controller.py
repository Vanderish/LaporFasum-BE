from fastapi import HTTPException
from app.core.database import get_db_connection

def get_all_kategori():
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id_kategori, nama_kategori FROM kategori_fasilitas")
        kategori_list = cursor.fetchall()
        return {"data": kategori_list}
    finally:
        cursor.close()
        db.close()

def get_kategori_by_id(id_kategori: int):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id_kategori, nama_kategori FROM kategori_fasilitas WHERE id_kategori = %s", (id_kategori,))
        kategori = cursor.fetchone()
        
        if not kategori:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
            
        return {"data": kategori}
    finally:
        cursor.close()
        db.close()
