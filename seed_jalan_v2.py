import urllib.request
import json
import ssl
import mysql.connector
import os
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com")
DB_PORT = int(os.getenv("DB_PORT", 4000))
DB_NAME = os.getenv("DB_NAME", "pelaporan")
DB_USER = os.getenv("DB_USER", "R4su5Rz44sbrb7h.root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ou1ZX2tkvojL1MgF")

CACHE_DIR = "/tmp/opencode/geojson_cache"

GEOJSON_URLS = {
    "arteri-primer": "https://skala.lamongankab.go.id/peta/geojsons/20240709_174127/Jalan%20Arteri%20Primer.geojson",
    "kolektor-primer-1": "https://skala.lamongankab.go.id/peta/geojsons/20240709_174127/Jalan%20Kolektor%20Primer%20Satu%20(JKP-1).geojson",
    "kolektor-primer-2": "https://skala.lamongankab.go.id/peta/geojsons/20240709_174127/Jalan%20Kolektor%20Primer%20Dua%20(JKP-2).geojson",
    "kolektor-primer-3": "https://skala.lamongankab.go.id/peta/geojsons/20240709_174127/Jalan%20Kolektor%20Primer%20Tiga%20(JKP-3).geojson",
    "arteri-sekunder": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Arteri%20Sekunder.geojson",
    "kolektor-primer-4": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Kolektor%20Primer%204.geojson",
    "kolektor-sekunder": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Kolektor%20Sekunder.geojson",
    "lingkungan-primer": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Lingkungan%20Primer.geojson",
    "lingkungan-sekunder": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Lingkungan%20Sekunder.geojson",
    "lokal-primer": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Lokal%20Primer.geojson",
    "lokal-sekunder": "https://skala.lamongankab.go.id/peta/geojsons/20260510_033012/Lokal%20Sekunder.geojson",
}

KATEGORI_TO_STATUS = {
    "arteri-primer": "Nasional",
    "kolektor-primer-1": "Provinsi",
    "kolektor-primer-2": "Provinsi",
    "kolektor-primer-3": "Provinsi",
    "arteri-sekunder": "Kabupaten",
    "kolektor-primer-4": "Kabupaten",
    "kolektor-sekunder": "Kabupaten",
    "lingkungan-primer": "Kecamatan",
    "lingkungan-sekunder": "Kecamatan",
    "lokal-primer": "Kecamatan",
    "lokal-sekunder": "Kecamatan",
}

os.makedirs(CACHE_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_geojson(kategori, url):
    cache_file = os.path.join(CACHE_DIR, f"{kategori}.json")
    
    if os.path.exists(cache_file):
        print(f"  [CACHE] Loading from {cache_file}")
        with open(cache_file, "r") as f:
            return json.load(f)
    
    try:
        print(f"  [FETCH] Downloading {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        with open(cache_file, "w") as f:
            json.dump(data, f)
        
        return data
    except Exception as e:
        print(f"  [ERROR] Fetch {url}: {e}")
        return []

def validate_coords(coords):
    if len(coords) < 2:
        return False, "Less than 2 points"
    
    for coord in coords:
        if len(coord) < 2:
            return False, "Coord has less than 2 values"
        lng, lat = coord[0], coord[1]
        if not (-180 <= lng <= 180):
            return False, f"Longitude {lng} out of range"
        if not (-90 <= lat <= 90):
            return False, f"Latitude {lat} out of range"
    
    return True, "OK"

def seed_jalan_v2():
    conn = mysql.connector.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, ssl_disabled=False, connect_timeout=30
    )
    cursor = conn.cursor()

    try:
        print(f"[{datetime.now()}] Creating jalan_v2 table...")
        with open("migrations/001_create_jalan_v2.sql", "r") as f:
            cursor.execute(f.read())
        conn.commit()
        print(f"[{datetime.now()}] Table created/verified")

        print(f"[{datetime.now()}] Truncating jalan_v2...")
        cursor.execute("TRUNCATE TABLE jalan_v2")
        conn.commit()

        total_inserted = 0
        total_skipped = 0

        for kategori, url in GEOJSON_URLS.items():
            print(f"\n[{datetime.now()}] Processing {kategori}...")
            features = fetch_geojson(kategori, url)
            status = KATEGORI_TO_STATUS[kategori]
            
            print(f"  Features count: {len(features)}")

            for i, feature in enumerate(features):
                try:
                    geom = feature.get("geometry", {})
                    coords = geom.get("coordinates", [])
                    props = feature.get("properties", {})

                    if geom.get("type") != "LineString":
                        total_skipped += 1
                        continue

                    valid, reason = validate_coords(coords)
                    if not valid:
                        total_skipped += 1
                        continue

                    nama_jalan = props.get("NAMOBJ") or props.get("NAMA_RUAS_") or f"{kategori}_{i}"
                    koordinat_lintasan = json.dumps(coords)
                    properties_json = json.dumps(props)

                    cursor.execute("""
                        INSERT INTO jalan_v2 
                        (nama_jalan, kategori_jalan, status_kepemilikan, koordinat_lintasan, properties, id_kabupaten, id_kategori)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        nama_jalan, kategori, status, koordinat_lintasan, properties_json, 1, 1
                    ))
                    total_inserted += 1

                    if total_inserted % 100 == 0:
                        conn.commit()
                        print(f"  Progress: {total_inserted} inserted, {total_skipped} skipped")

                except Exception as e:
                    print(f"  [ERROR] Feature {i}: {e}")
                    total_skipped += 1
                    continue

            conn.commit()
            print(f"  Kategori {kategori} done: {total_inserted} total so far")

        print(f"\n[{datetime.now()}] ========== SUMMARY ==========")
        print(f"Total Inserted: {total_inserted}")
        print(f"Total Skipped: {total_skipped}")
        print(f"Total: {total_inserted + total_skipped}")

        cursor.execute("SELECT COUNT(*) as cnt FROM jalan_v2")
        final_count = cursor.fetchone()[0]
        print(f"Final DB Count: {final_count}")
        print(f"[{datetime.now()}] ===== SEED COMPLETE =====")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_jalan_v2()
