from fastapi import HTTPException, UploadFile, File, Form
from app.core.database import get_db_connection
from app.core.security import get_password_hash
import cloudinary.uploader
from typing import Optional, List
import os

def create_laporan(
    judul_laporan: str = Form(...),
    deskripsi: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    id_kategori: int = Form(...),
    id_kecamatan_kejadian: Optional[int] = Form(None),
    foto_bukti: UploadFile = File(...),
    current_user: dict = None
):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        # Upload foto ke Cloudinary
        upload_result = cloudinary.uploader.upload(foto_bukti.file, folder="laporan_fasilitas")
        foto_url = upload_result.get("secure_url")
        
        id_user = current_user.get("id_user")
        if not id_kecamatan_kejadian:
            id_kecamatan_kejadian = current_user.get("id_kecamatan")
        
        cursor.execute("""
            INSERT INTO laporan (judul_laporan, deskripsi, foto_bukti, latitude, longitude, status_terkini, id_kategori, id_kecamatan_kejadian, id_user)
            VALUES (%s, %s, %s, %s, %s, 'Menunggu Verifikasi', %s, %s, %s)
        """, (judul_laporan, deskripsi, foto_url, latitude, longitude, id_kategori, id_kecamatan_kejadian, id_user))
        db.commit()
        
        id_laporan = cursor.lastrowid
        
        # Insert ke riwayat_status_laporan
        cursor.execute("""
            INSERT INTO riwayat_status_laporan (id_laporan, status_sebelum, status_sesudah, kewenangan_penanganan, tanggapan_admin)
            VALUES (%s, '', 'Menunggu Verifikasi', '', 'Laporan baru dibuat')
        """, (id_laporan,))
        db.commit()
        
        return {"message": "Laporan berhasil dibuat", "id_laporan": id_laporan}
    finally:
        cursor.close()
        db.close()

def get_laporan_list(
    current_user: dict,
    status: Optional[str] = None,
    kategori: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        id_role = current_user.get("id_role")
        id_kecamatan = current_user.get("id_kecamatan")
        id_user = current_user.get("id_user")
        
        query = """
            SELECT l.*, k.nama_kategori, kec.nama_kecamatan
            FROM laporan l
            JOIN kategori_fasilitas k ON l.id_kategori = k.id_kategori
            JOIN kecamatan kec ON l.id_kecamatan_kejadian = kec.id_kecamatan
            WHERE 1=1
        """
        params = []
        
        if id_role == 1:
            query += " AND l.id_pelapor = %s"
            params.append(id_user)
        elif id_role == 2:
            query += " AND l.id_kecamatan_kejadian = %s"
            params.append(id_kecamatan)
        elif id_role not in [2, 3]:
            raise HTTPException(status_code=403, detail="Akses ditolak")
        
        if status:
            query += " AND l.status_terkini = %s"
            params.append(status)
        
        if kategori:
            query += " AND l.id_kategori = %s"
            params.append(kategori)
        
        if search:
            query += " AND (l.judul_laporan LIKE %s OR l.deskripsi LIKE %s)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        count_query = query.replace("SELECT l.*, k.nama_kategori, kec.nama_kecamatan", "SELECT COUNT(*) as total")
        cursor.execute(count_query, tuple(params))
        total = cursor.fetchone()["total"]
        
        offset = (page - 1) * limit
        query += " ORDER BY l.created_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, tuple(params))
        laporan_list = cursor.fetchall()
        
        return {
            "data": laporan_list,
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

def get_laporan_saya(current_user: dict):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        id_user = current_user.get("id_user")
        
        query = """
            SELECT l.*, k.nama_kategori, kec.nama_kecamatan
            FROM laporan l
            JOIN kategori_fasilitas k ON l.id_kategori = k.id_kategori
            JOIN kecamatan kec ON l.id_kecamatan_kejadian = kec.id_kecamatan
            WHERE l.id_pelapor = %s
            ORDER BY l.created_at DESC
        """
        cursor.execute(query, (id_user,))
        laporan_list = cursor.fetchall()
        return {"data": laporan_list}
    finally:
        cursor.close()
        db.close()

def get_laporan_by_id(id_laporan: int, current_user: dict):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        query = """
            SELECT l.*, k.nama_kategori, kec.nama_kecamatan, u.nama_lengkap
            FROM laporan l
            JOIN kategori_fasilitas k ON l.id_kategori = k.id_kategori
            JOIN kecamatan kec ON l.id_kecamatan_kejadian = kec.id_kecamatan
            JOIN users u ON l.id_pelapor = u.id_user
            WHERE l.id_laporan = %s
        """
        cursor.execute(query, (id_laporan,))
        laporan = cursor.fetchone()
        
        if not laporan:
            raise HTTPException(status_code=404, detail="Laporan tidak ditemukan")
        
        # RBAC check
        id_role = current_user.get("id_role")
        id_kecamatan = current_user.get("id_kecamatan")
        id_user = current_user.get("id_user")
        
        if id_role == 1 and laporan["id_pelapor"] != id_user:
            # Warga hanya bisa lihat laporan sendiri kalau bukan publik
            if laporan["status_terkini"] == "Ditolak":
                raise HTTPException(status_code=403, detail="Akses ditolak")
        elif id_role == 2 and laporan["id_kecamatan_kejadian"] != id_kecamatan:
            raise HTTPException(status_code=403, detail="Akses ditolak: Bukan wilayah Anda")
        
        return {"data": laporan}
    finally:
        cursor.close()
        db.close()

def update_laporan_status(id_laporan: int, status_terkini: str, kewenangan_penanganan: str, tanggapan_admin: Optional[str] = None, current_user: dict = None):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        # Validasi role admin
        id_role = current_user.get("id_role")
        if id_role not in [2, 3]:
            raise HTTPException(status_code=403, detail="Hanya admin yang bisa mengubah status")
        
        # Validasi status
        valid_status = ["Menunggu Verifikasi", "Diterima", "Ditolak", "Diproses", "Selesai"]
        if status_terkini not in valid_status:
            raise HTTPException(status_code=400, detail="Status tidak valid")
        
        # Validasi kewenangan
        valid_kewenangan = ["Kecamatan", "Kabupaten"]
        if kewenangan_penanganan not in valid_kewenangan:
            raise HTTPException(status_code=400, detail="Kewenangan penanganan tidak valid")
        
        # Ambil status lama
        cursor.execute("SELECT status_terkini FROM laporan WHERE id_laporan = %s", (id_laporan,))
        laporan = cursor.fetchone()
        
        if not laporan:
            raise HTTPException(status_code=404, detail="Laporan tidak ditemukan")
        
        status_lama = laporan["status_terkini"]
        
        # Update laporan
        cursor.execute("""
            UPDATE laporan 
            SET status_terkini = %s, kewenangan_penanganan = %s
            WHERE id_laporan = %s
        """, (status_terkini, kewenangan_penanganan, id_laporan))
        
        # Insert ke riwayat
        cursor.execute("""
            INSERT INTO riwayat_status_laporan (id_laporan, id_admin_pemroses, status_update, tanggapan_admin)
            VALUES (%s, %s, %s, %s)
        """, (id_laporan, current_user.get("id_user"), status_terkini, tanggapan_admin or f"Status diubah dari {status_lama} ke {status_terkini}"))
        
        db.commit()
        return {"message": "Status laporan berhasil diperbarui"}
    finally:
        cursor.close()
        db.close()

def get_riwayat_laporan(id_laporan: int, current_user: dict):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        # Cek laporan exists
        cursor.execute("SELECT id_laporan FROM laporan WHERE id_laporan = %s", (id_laporan,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Laporan tidak ditemukan")
        
        query = """
            SELECT * FROM riwayat_status_laporan 
            WHERE id_laporan = %s 
            ORDER BY created_at ASC
        """
        cursor.execute(query, (id_laporan,))
        riwayat = cursor.fetchall()
        return {"data": riwayat}
    finally:
        cursor.close()
        db.close()

def delete_laporan(id_laporan: int, current_user: dict):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        # Cek laporan exists
        cursor.execute("SELECT id_pelapor, status_terkini FROM laporan WHERE id_laporan = %s", (id_laporan,))
        laporan = cursor.fetchone()
        
        if not laporan:
            raise HTTPException(status_code=404, detail="Laporan tidak ditemukan")
        
        id_user = current_user.get("id_user")
        id_role = current_user.get("id_role")
        
        if id_role == 1 and laporan["id_pelapor"] != id_user:
            raise HTTPException(status_code=403, detail="Hanya pelapor yang bisa menghapus laporan")
        
        if laporan["status_terkini"] not in ["Menunggu Verifikasi"]:
            raise HTTPException(status_code=400, detail="Hanya laporan Menunggu Verifikasi yang bisa dihapus")
        
        cursor.execute("DELETE FROM laporan WHERE id_laporan = %s", (id_laporan,))
        db.commit()
        
        return {"message": "Laporan berhasil dihapus"}
    finally:
        cursor.close()
        db.close()