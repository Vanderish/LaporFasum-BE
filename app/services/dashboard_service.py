from app.core.database import get_db_connection
from fastapi import HTTPException
from typing import List, Dict, Any


def get_warga_statistik(current_user: dict) -> Dict[str, Any]:
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")

    cursor = db.cursor(dictionary=True)

    try:
        id_kecamatan = current_user.get("id_kecamatan")

        query_statistik_wilayah = """
            SELECT 
                COUNT(id_laporan) AS total_laporan,
                SUM(CASE WHEN status_terkini = 'Diterima' THEN 1 ELSE 0 END) AS diproses,
                SUM(CASE WHEN status_terkini = 'Selesai' THEN 1 ELSE 0 END) AS selesai
            FROM laporan 
            WHERE id_kecamatan_kejadian = %s
        """
        cursor.execute(query_statistik_wilayah, (id_kecamatan,))
        statistik_result = cursor.fetchone()

        statistik_wilayah = {
            "total_laporan": int(statistik_result["total_laporan"] or 0) if statistik_result else 0,
            "diproses": int(statistik_result["diproses"] or 0) if statistik_result else 0,
            "selesai": int(statistik_result["selesai"] or 0) if statistik_result else 0
        }

        query_harian = """
            SELECT DATE(created_at) AS tanggal, COUNT(id_laporan) AS jumlah
            FROM laporan
            WHERE id_kecamatan_kejadian = %s
              AND created_at >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DATE(created_at)
            ORDER BY tanggal
        """
        cursor.execute(query_harian, (id_kecamatan,))
        statistik_harian = cursor.fetchall()

        query_mingguan = """
            SELECT YEARWEEK(created_at, 1) AS minggu, COUNT(id_laporan) AS jumlah
            FROM laporan
            WHERE id_kecamatan_kejadian = %s
              AND created_at >= DATE_SUB(CURDATE(), INTERVAL 3 WEEK)
            GROUP BY YEARWEEK(created_at, 1)
            ORDER BY minggu
        """
        cursor.execute(query_mingguan, (id_kecamatan,))
        statistik_mingguan = cursor.fetchall()

        query_bulanan = """
            SELECT DATE_FORMAT(created_at, '%Y-%m') AS bulan, COUNT(id_laporan) AS jumlah
            FROM laporan
            WHERE id_kecamatan_kejadian = %s
              AND created_at >= DATE_SUB(CURDATE(), INTERVAL 5 MONTH)
            GROUP BY DATE_FORMAT(created_at, '%Y-%m')
            ORDER BY bulan
        """
        cursor.execute(query_bulanan, (id_kecamatan,))
        statistik_bulanan = cursor.fetchall()

        return {
            "statistik_wilayah": statistik_wilayah,
            "statistik_harian": statistik_harian,
            "statistik_mingguan": statistik_mingguan,
            "statistik_bulanan": statistik_bulanan
        }
    finally:
        cursor.close()
        db.close()


def get_warga_laporan_terbaru(current_user: dict) -> List[Dict[str, Any]]:
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")

    cursor = db.cursor(dictionary=True)

    try:
        id_user = current_user.get("id_user")

        query_laporan_terbaru = """
            SELECT l.id_laporan, l.judul_laporan, l.deskripsi_laporan, l.foto_bukti, l.status_terkini, l.created_at AS waktu_lapor,
                   k.nama_kategori, kec.nama_kecamatan
            FROM laporan l
            LEFT JOIN kategori_fasilitas k ON l.id_kategori = k.id_kategori
            JOIN kecamatan kec ON l.id_kecamatan_kejadian = kec.id_kecamatan
            WHERE l.id_pelapor = %s
            ORDER BY l.created_at DESC
            LIMIT 5
        """
        cursor.execute(query_laporan_terbaru, (id_user,))
        laporan_terbaru = cursor.fetchall()
        return laporan_terbaru
    finally:
        cursor.close()
        db.close()


def get_admin_statistik(current_user: dict) -> Dict[str, Any]:
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")

    cursor = db.cursor(dictionary=True)

    try:
        id_role = current_user.get("id_role")
        id_kecamatan = current_user.get("id_kecamatan")

        where_kecamatan = ""
        params = []
        if id_role == 2 or (id_role == 3 and id_kecamatan):
            where_kecamatan = "WHERE id_kecamatan_kejadian = %s"
            params.append(id_kecamatan)

        query_status = f"""
            SELECT 
                SUM(CASE WHEN status_terkini = 'Menunggu Verifikasi' THEN 1 ELSE 0 END) AS menunggu,
                SUM(CASE WHEN status_terkini = 'Diterima' THEN 1 ELSE 0 END) AS diterima,
                SUM(CASE WHEN status_terkini = 'Ditolak' THEN 1 ELSE 0 END) AS ditolak,
                SUM(CASE WHEN status_terkini = 'Diproses' THEN 1 ELSE 0 END) AS diproses,
                SUM(CASE WHEN status_terkini = 'Selesai' THEN 1 ELSE 0 END) AS selesai
            FROM laporan
            {where_kecamatan}
        """
        cursor.execute(query_status, tuple(params))
        status_result = cursor.fetchone()

        statistik_status = {
            "menunggu": int(status_result["menunggu"] or 0) if status_result else 0,
            "diterima": int(status_result["diterima"] or 0) if status_result else 0,
            "ditolak": int(status_result["ditolak"] or 0) if status_result else 0,
            "diproses": int(status_result["diproses"] or 0) if status_result else 0,
            "selesai": int(status_result["selesai"] or 0) if status_result else 0
        }

        query_kategori = f"""
            SELECT k.nama_kategori, COUNT(l.id_laporan) AS jumlah_laporan
            FROM laporan l
            LEFT JOIN kategori_fasilitas k ON l.id_kategori = k.id_kategori
            {where_kecamatan}
            GROUP BY k.id_kategori, k.nama_kategori
            ORDER BY jumlah_laporan DESC
        """
        cursor.execute(query_kategori, tuple(params))
        rekapitulasi_kategori = cursor.fetchall()

        hari_labels = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"]
        query_harian = f"""
            SELECT 
                DAYOFWEEK(created_at) AS hari_ke,
                COUNT(id_laporan) AS jumlah
            FROM laporan
            {where_kecamatan}
            {'AND' if where_kecamatan else 'WHERE'} created_at >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            GROUP BY DAYOFWEEK(created_at)
            ORDER BY hari_ke
        """
        cursor.execute(query_harian, tuple(params))
        harian_raw = {row["hari_ke"]: row["jumlah"] for row in cursor.fetchall()}

        statistik_harian = []
        for i in range(1, 8):
            label_idx = (i - 1) % 7
            statistik_harian.append({
                "label": hari_labels[label_idx],
                "value": int(harian_raw.get(i, 0))
            })

        query_mingguan = """
            SELECT 
                YEARWEEK(created_at, 1) AS minggu,
                COUNT(id_laporan) AS jumlah
            FROM laporan
            {where_kecamatan}
            {where_and} created_at >= DATE_SUB(CURDATE(), INTERVAL 3 WEEK)
            GROUP BY YEARWEEK(created_at, 1)
            ORDER BY minggu
        """.format(where_kecamatan=where_kecamatan, where_and='AND' if where_kecamatan else 'WHERE')
        cursor.execute(query_mingguan, tuple(params))
        mingguan_raw = cursor.fetchall()

        statistik_bulanan = []
        for idx, row in enumerate(mingguan_raw):
            statistik_bulanan.append({
                "label": f"Minggu {idx + 1}",
                "value": int(row["jumlah"] or 0)
            })

        while len(statistik_bulanan) < 4:
            statistik_bulanan.append({"label": f"Minggu {len(statistik_bulanan) + 1}", "value": 0})

        return {
            "statistik_status": statistik_status,
            "rekapitulasi_kategori": rekapitulasi_kategori,
            "statistik_harian": statistik_harian,
            "statistik_bulanan": statistik_bulanan
        }
    finally:
        cursor.close()
        db.close()