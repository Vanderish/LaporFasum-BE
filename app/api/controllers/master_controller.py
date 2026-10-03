from fastapi import HTTPException
from app.core.database import get_db_connection
from typing import Optional, List

def get_all_kecamatan(page: int = 1, limit: int = 50):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as total FROM kecamatan")
        total = cursor.fetchone()["total"]
        
        offset = (page - 1) * limit
        cursor.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan ORDER BY nama_kecamatan LIMIT %s OFFSET %s", (limit, offset))
        kecamatan_list = cursor.fetchall()
        
        return {
            "data": kecamatan_list,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        }
    finally:
        cursor.close()
        db.close()

def get_all_kategori(page: int = 1, limit: int = 50):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as total FROM kategori_fasilitas")
        total = cursor.fetchone()["total"]
        
        offset = (page - 1) * limit
        cursor.execute("SELECT id_kategori, nama_kategori FROM kategori_fasilitas ORDER BY nama_kategori LIMIT %s OFFSET %s", (limit, offset))
        kategori_list = cursor.fetchall()
        
        return {
            "data": kategori_list,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        }
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

def get_fasilitas_umum(nama: Optional[str] = None, kategori: Optional[int] = None, page: int = 1, limit: int = 20):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        query = """
            SELECT id_fasilitas_umum as id_fasilitas, nama_fasilitas, id_kategori, latitude, longitude 
            FROM fasilitas_umum 
            WHERE 1=1
        """
        params = []
        
        if nama:
            query += " AND nama_fasilitas LIKE %s"
            params.append(f"%{nama}%")
        if kategori:
            query += " AND id_kategori = %s"
            params.append(kategori)
        
        count_query = query.replace("SELECT id_fasilitas_umum as id_fasilitas, nama_fasilitas, id_kategori, latitude, longitude", "SELECT COUNT(*) as total")
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()["total"]
        
        offset = (page - 1) * limit
        query += " ORDER BY nama_fasilitas LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, tuple(params))
        fasilitas_list = cursor.fetchall()
        
        return {
            "data": fasilitas_list,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        }
    finally:
        cursor.close()
        db.close()

def get_rute_fasilitas(id_fasilitas: int):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        # Cek fasilitas ada
        cursor.execute("SELECT id_fasilitas_umum as id_fasilitas, nama_fasilitas FROM fasilitas_umum WHERE id_fasilitas_umum = %s", (id_fasilitas,))
        fasilitas = cursor.fetchone()
        
        if not fasilitas:
            raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
        
        # Cek di detail_jalan_nasional
        cursor.execute("""
            SELECT koordinat_lintasan 
            FROM detail_jalan_nasional 
            WHERE id_fasilitas_umum = %s 
        """, (id_fasilitas,))
        result = cursor.fetchone()
        
        koordinat = []
        if result and result.get('koordinat_lintasan'):
            import json
            try:
                coords = json.loads(result['koordinat_lintasan'])
                for coord in coords:
                    if len(coord) >= 2:
                        koordinat.append({"latitude": coord[1], "longitude": coord[0]})
            except:
                pass
        
        # Kalau kosong, cek detail_fungsi_jalan
        if not koordinat:
            cursor.execute("""
                SELECT koordinat_lintasan 
                FROM detail_fungsi_jalan 
                WHERE id_fasilitas_umum = %s 
            """, (id_fasilitas,))
            result = cursor.fetchone()
            if result and result.get('koordinat_lintasan'):
                import json
                try:
                    coords = json.loads(result['koordinat_lintasan'])
                    for coord in coords:
                        if len(coord) >= 2:
                            koordinat.append({"latitude": coord[1], "longitude": coord[0]})
                except:
                    pass
        
        return {
            "id_fasilitas": fasilitas["id_fasilitas"],
            "nama_fasilitas": fasilitas["nama_fasilitas"],
            "koordinat": koordinat
        }
    finally:
        cursor.close()
        db.close()