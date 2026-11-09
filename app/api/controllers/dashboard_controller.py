from fastapi import HTTPException
from app.core.database import get_db_connection
from typing import List, Dict, Any
from app.services import dashboard_service


def get_dashboard_warga(current_user: dict):
    statistik = dashboard_service.get_warga_statistik(current_user)
    laporan_terbaru = dashboard_service.get_warga_laporan_terbaru(current_user)
    
    return {
        **statistik,
        "laporan_terbaru": laporan_terbaru
    }


def get_dashboard_admin(current_user: dict):
    data = dashboard_service.get_admin_statistik(current_user)
    return {
        "status": "success",
        "data": data
    }


def get_heatmap_data():
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")

    cursor = db.cursor(dictionary=True)

    try:
        query = """
            SELECT latitude, longitude 
            FROM laporan 
            WHERE status_terkini NOT IN ('Ditolak', 'Selesai')
              AND latitude IS NOT NULL 
              AND longitude IS NOT NULL
        """
        cursor.execute(query)
        points = cursor.fetchall()

        latitude = [float(p["latitude"]) for p in points]
        longitude = [float(p["longitude"]) for p in points]

        return {
            "latitude": latitude,
            "longitude": longitude
        }
    finally:
        cursor.close()
        db.close()


def get_notifikasi(current_user: dict, page: int = 1, limit: int = 10):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")

    cursor = db.cursor(dictionary=True)

    try:
        id_user = current_user.get("id_user")

        count_query = "SELECT COUNT(*) as total FROM notifikasi WHERE id_user = %s"
        cursor.execute(count_query, (id_user,))
        total = cursor.fetchone()["total"]

        offset = (page - 1) * limit
        query = """
            SELECT id_notifikasi, id_laporan, judul, pesan, tipe_notifikasi, is_read, created_at
            FROM notifikasi
            WHERE id_user = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (id_user, limit, offset))
        notifikasi = cursor.fetchall()

        return {
            "data": notifikasi,
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