from fastapi import HTTPException, Query
from app.core.database import get_db_connection
import json
import os

def get_batas_wilayah():
    geojson_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "batas_wilayah_lamongan.geojson")
    geojson_path = os.path.normpath(geojson_path)
    
    if os.path.exists(geojson_path):
        with open(geojson_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Fallback: return empty FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": []
    }

def get_infrastruktur(kepemilikan: str = None, page: int = 1, limit: int = 100):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        features = []
        
        # Query detail_jalan_nasional
        query_nasional = """
            SELECT djn.koordinat_lintasan, djn.namobj, fu.status_kepemilikan, djn.id_jalan_nasional as id_fasilitas
            FROM detail_jalan_nasional djn
            JOIN fasilitas_umum fu ON djn.id_fasilitas_umum = fu.id_fasilitas_umum
        """
        params_nasional = []
        
        if kepemilikan:
            query_nasional += " WHERE fu.status_kepemilikan = %s"
            params_nasional.append(kepemilikan)
            
        count_nasional = query_nasional.replace("SELECT djn.koordinat_lintasan, djn.namobj, fu.status_kepemilikan, djn.id_jalan_nasional as id_fasilitas", "SELECT COUNT(*) as total")
        cursor.execute(count_nasional, tuple(params_nasional))
        total_nasional = cursor.fetchone()["total"]
        
        offset = (page - 1) * limit
        query_nasional += " LIMIT %s OFFSET %s"
        params_nasional.extend([limit, offset])
        
        cursor.execute(query_nasional, tuple(params_nasional))
        rows_nasional = cursor.fetchall()
        
        for row in rows_nasional:
            if row.get('koordinat_lintasan'):
                try:
                    coords = json.loads(row['koordinat_lintasan'])
                    if coords and len(coords) >= 2:
                        features.append({
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": coords
                            },
                            "properties": {
                                "nama_jalan": row.get('namobj', ''),
                                "kepemilikan": row.get('status_kepemilikan', 'Nasional'),
                                "id_fasilitas": row.get('id_fasilitas')
                            }
                        })
                except:
                    pass
        
        # Query detail_fungsi_jalan
        query_fungsi = """
            SELECT dfj.koordinat_lintasan, dfj.nama_ruas, fu.status_kepemilikan, dfj.id_fungsi_jalan as id_fasilitas
            FROM detail_fungsi_jalan dfj
            JOIN fasilitas_umum fu ON dfj.id_fasilitas_umum = fu.id_fasilitas_umum
        """
        params_fungsi = []
        
        if kepemilikan:
            query_fungsi += " WHERE fu.status_kepemilikan = %s"
            params_fungsi.append(kepemilikan)
            
        count_fungsi = query_fungsi.replace("SELECT dfj.koordinat_lintasan, dfj.nama_ruas, fu.status_kepemilikan, dfj.id_fungsi_jalan as id_fasilitas", "SELECT COUNT(*) as total")
        cursor.execute(count_fungsi, tuple(params_fungsi))
        total_fungsi = cursor.fetchone()["total"]
        
        query_fungsi += " LIMIT %s OFFSET %s"
        params_fungsi.extend([limit, offset])
        
        cursor.execute(query_fungsi, tuple(params_fungsi))
        rows_fungsi = cursor.fetchall()
        
        for row in rows_fungsi:
            if row.get('koordinat_lintasan'):
                try:
                    coords = json.loads(row['koordinat_lintasan'])
                    if coords and len(coords) >= 2:
                        features.append({
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": coords
                            },
                            "properties": {
                                "nama_jalan": row.get('nama_ruas', ''),
                                "kepemilikan": row.get('status_kepemilikan', ''),
                                "id_fasilitas": row.get('id_fasilitas')
                            }
                        })
                except:
                    pass
        
        total = total_nasional + total_fungsi
        
        return {
            "type": "FeatureCollection",
            "features": features,
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

def get_titik_laporan(page: int = 1, limit: int = 100):
    db = get_db_connection()
    if not db:
        raise HTTPException(status_code=500, detail="Koneksi database gagal")
        
    cursor = db.cursor(dictionary=True)
    
    try:
        query = """
            SELECT l.id_laporan, l.judul_laporan, l.latitude, l.longitude, 
                   l.status_terkini, k.nama_kategori, l.kewenangan_penanganan
            FROM laporan l
            JOIN kategori_fasilitas k ON l.id_kategori = k.id_kategori
            WHERE l.status_terkini IN ('Menunggu Verifikasi', 'Diterima', 'Diproses')
        """
        
        count_query = query.replace("SELECT l.id_laporan, l.judul_laporan, l.latitude, l.longitude, l.status_terkini, k.nama_kategori, l.kewenangan_penanganan", "SELECT COUNT(*) as total")
        cursor.execute(count_query)
        total = cursor.fetchone()["total"]
        
        offset = (page - 1) * limit
        query += " ORDER BY l.created_at DESC LIMIT %s OFFSET %s"
        
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()
        
        features = []
        for row in rows:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(row['longitude']), float(row['latitude'])]
                },
                "properties": {
                    "id_laporan": row['id_laporan'],
                    "judul_laporan": row['judul_laporan'],
                    "status_terkini": row['status_terkini'],
                    "kategori": row['nama_kategori'],
                    "kewenangan_penanganan": row['kewenangan_penanganan']
                }
            })
        
        return {
            "type": "FeatureCollection",
            "features": features,
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