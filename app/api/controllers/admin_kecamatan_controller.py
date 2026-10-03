from fastapi import HTTPException
from app.core.database import get_db_connection

def get_dashboard_data(current_user: dict, page: int = 1, limit: int = 10):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        id_kecamatan = current_user.get("id_kecamatan")
        
        # 1. Kartu Statistik
        query_statistik = """
        SELECT 
            COUNT(id_laporan) AS total_laporan,
            SUM(CASE WHEN status_terkini = 'Menunggu Verifikasi' THEN 1 ELSE 0 END) AS menunggu,
            SUM(CASE WHEN status_terkini = 'Diterima' THEN 1 ELSE 0 END) AS diproses,
            SUM(CASE WHEN status_terkini = 'Selesai' THEN 1 ELSE 0 END) AS selesai
        FROM laporan 
        WHERE id_kecamatan_kejadian = %s;
        """
        cursor.execute(query_statistik, (id_kecamatan,))
        statistik_result = cursor.fetchone()
        
        # Menangani nilai NULL/None dari fungsi SUM di MySQL
        statistik = {
            "total_laporan": int(statistik_result["total_laporan"] or 0) if statistik_result else 0,
            "menunggu": int(statistik_result["menunggu"] or 0) if statistik_result else 0,
            "diproses": int(statistik_result["diproses"] or 0) if statistik_result else 0,
            "selesai": int(statistik_result["selesai"] or 0) if statistik_result else 0
        }
        
        # 2. Grafik Laporan Mingguan
        query_grafik = """
        SELECT 
            DAYNAME(created_at) AS hari,
            COUNT(id_laporan) AS jumlah_laporan
        FROM laporan
        WHERE id_kecamatan_kejadian = %s
          AND YEARWEEK(created_at, 1) = YEARWEEK(CURDATE(), 1)
        GROUP BY DAYOFWEEK(created_at), hari
        ORDER BY DAYOFWEEK(created_at);
        """
        cursor.execute(query_grafik, (id_kecamatan,))
        grafik_mingguan = cursor.fetchall()
        
        # 3. Daftar Laporan (paginated)
        query_daftar = """
        SELECT 
            l.id_laporan,
            l.judul_laporan,
            l.foto_bukti,
            l.status_terkini,
            l.created_at AS waktu_lapor,
            r.tanggapan_admin,
            r.created_at AS waktu_update_terakhir
        FROM laporan l
        LEFT JOIN riwayat_status_laporan r 
            ON l.id_laporan = r.id_laporan 
            AND r.id_riwayat = (
                SELECT MAX(id_riwayat) 
                FROM riwayat_status_laporan 
                WHERE id_laporan = l.id_laporan
            )
        WHERE l.id_kecamatan_kejadian = %s
        ORDER BY l.created_at DESC
        LIMIT %s OFFSET %s;
        """
        offset = (page - 1) * limit
        cursor.execute(query_daftar, (id_kecamatan, limit, offset))
        daftar_laporan = cursor.fetchall()
        
        # Total count for pagination
        cursor.execute("SELECT COUNT(*) as total FROM laporan WHERE id_kecamatan_kejadian = %s", (id_kecamatan,))
        total = cursor.fetchone()["total"]
        
        return {
            "statistik": statistik,
            "grafik_mingguan": grafik_mingguan,
            "daftar_laporan": daftar_laporan,
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
