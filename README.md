# Sistem Pelaporan Fasilitas Umum Kabupaten Lamongan

Platform digital untuk pelaporan, monitoring, dan pengelolaan fasilitas umum di Kabupaten Lamongan. Sistem ini mengintegrasikan data pemetaan, infrastruktur jalan dari GeoJSON, serta memfasilitasi pelaporan berbasis komunitas dengan sistem verifikasi multi-level.

## Update Terbaru (v2.0)

- **Cloudinary Integration**: Upload dan manajemen gambar laporan fasilitas
- **Enhanced GIS Mapping**: Integrasi Mapbox & Overpass API untuk data jalan lengkap
- **Multi-role Dashboard**: Admin Kecamatan & Admin Kabupaten dengan akses berbeda
- **Real-time Notifications**: Sistem notifikasi status laporan
- **Jalan Nasional & Lokal**: Sinkronisasi data dari GeoJSON & OpenStreetMap
- **API Documentation**: Swagger UI di `/docs` dan ReDoc di `/redoc`

## Deskripsi

Sistem ini dirancang untuk:
- Mengumpulkan dan mengelola data fasilitas umum (kesehatan, pendidikan, transportasi, dll)
- Memproses laporan kerusakan/keluhan dari masyarakat
- Memberikan dashboard monitoring untuk admin tingkat kecamatan dan kabupaten
- Mengintegrasikan data infrastruktur jalan (nasional dan lokal)
- Mendukung analisis spasial dan pelaporan berbasis GIS

## Requirements

- Python 3.10+
- MariaDB 10.5+ atau MySQL 8.0+
- Node.js (opsional, jika ada frontend)
- Cloudinary Account (untuk upload gambar)
- Mapbox Access Token (opsional, untuk peta)

## Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd projek2
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
Salin file `.env.example` menjadi `.env` dan sesuaikan nilai variabel:

```bash
cp .env.example .env
```

Isi nilai-nilai berikut di file `.env`:
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`: Konfigurasi database
- `DB_NAME`: Nama database (default: `pelaporan`)
- `GEMINI_API_KEY`: API key untuk Gemini (opsional)
- `USER_SECRET`, `ADMIN_KEC_SECRET`, `ADMIN_KAB_SECRET`: JWT secrets (generate dengan `openssl rand -hex 64`)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: Konfigurasi Cloudinary untuk upload gambar
- `BOUNDINGBOX`: Bounding box peta Kabupaten Lamongan (default sudah terisi)
- `OVERPASS_URL`: Endpoint Overpass API untuk data OSM (default sudah terisi)

### 5. Setup Database
```bash
# Jalankan SQL dump untuk membuat struktur database
mysql -u root < pelaporan.sql

# atau jika menggunakan MariaDB
mariadb -u root < pelaporan.sql
```

## Struktur Database

### Tabel Utama
- **fasilitas_umum**: Data fasilitas publik dengan FK ke kategori dan instansi
- **laporan**: Laporan kerusakan/keluhan dari masyarakat
- **users**: Data pengguna sistem
- **roles**: Role pengguna (User, Admin Kecamatan, Admin Kabupaten)
- **kategori_fasilitas**: Klasifikasi jenis fasilitas
- **instansi_kewenangan**: Daftar instansi penanggungjawab
- **detail_jalan_nasional**: Rincian jalan nasional/provinsi
- **detail_fungsi_jalan**: Rincian jalan lokal/kabupaten

## Menjalankan Aplikasi

### Development Server
```bash
python main.py
```

Akses di: `http://localhost:8000`

### API Documentation
Dokumentasi API tersedia di:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Menjalankan dengan VS Code Port Forwarding

Jika menjalankan di remote server (Codespaces, SSH, Docker, WSL), gunakan **VS Code Port Forwarding**:

1. **Buka terminal di VS Code** (`Ctrl + `` ` ``)
2. **Jalankan server**:
   ```bash
   python main.py
   ```
3. **Port forwarding otomatis**: VS Code akan mendeteksi port 8000 dan menampilkan notifikasi "Port 8000 is now available"
4. **Klik "Open in Browser"** pada notifikasi, atau:
   - Buka panel **Ports** (`Ctrl+Shift+P` → "Ports: Focus on Ports View")
   - Klik ikon **globe** di kolom "Forwarded Address" untuk port 8000
   - Atau klik kanan port 8000 → "Preview in Editor" / "Open in Browser"

**Manual Port Forwarding** (jika tidak otomatis):
1. Panel **Ports** → klik **"Forward a Port"**
2. Masukkan `8000` → Enter
3. Klik kanan port 8000 → **"Port Visibility"** → **"Public"** (agar bisa diakses dari luar)

**Akses dari perangkat lain (HP/Tablet)**:
- Set Port Visibility ke **Public**
- Gunakan URL yang ditampilkan di kolom "Forwarded Address" (format: `https://<kode>-8000.<domain>.devtunnels.ms`)
- URL ini bisa dibuka dari perangkat mana saja di jaringan yang sama

**Troubleshooting Port Forwarding**:
- Pastikan `uvicorn` berjalan di `0.0.0.0:8000` (bukan `127.0.0.1:8000`)
- Di `main.py`, pastikan tidak ada host binding spesifik
- Restart VS Code / reload window jika port tidak terdeteksi

## Struktur Direktori

```
projek2/
├── app/
│   ├── core/           # Konfigurasi inti (database, security)
│   ├── models/         # Model database
│   ├── schemas/        # Pydantic schemas
│   ├── api/
│   │   ├── controllers/  # Business logic controllers
│   │   └── routes/       # Endpoint API routes
│   └── services/       # External services (AI, dll)
├── main.py             # Entry point aplikasi
├── seeder_jalan.py     # Script sinkronisasi data jalan
├── .env.example        # Template environment variables
├── requirements.txt    # Dependencies Python
└── pelaporan.sql       # Database dump
```

## Tech Stack

- **Backend**: FastAPI
- **Database**: MariaDB/MySQL
- **ORM/Connector**: mysql-connector-python, SQLAlchemy, PyMySQL
- **Authentication**: JWT (python-jose)
- **API Integration**: Gemini, Mapbox, Overpass API
- **Image Storage**: Cloudinary
- **Data Format**: GeoJSON
- **Server**: Uvicorn
- **Validation**: Pydantic v2

## User Roles

1. **User**: Dapat membuat dan melihat laporan pribadi
2. **Admin Kecamatan**: Verifikasi dan tanggapi laporan di tingkat kecamatan
3. **Admin Kabupaten**: Monitoring keseluruhan dan pelaporan kabupaten

## Fitur Utama

- Dashboard monitoring fasilitas publik (Admin Kecamatan & Kabupaten)
- Sistem pelaporan kerusakan/keluhan terukur dengan foto
- Verifikasi multi-level oleh admin (Kecamatan → Kabupaten)
- Integrasi pemetaan berbasis GIS (Mapbox + Overpass API)
- Tracking riwayat status laporan real-time
- Notifikasi real-time status laporan
- Upload & manajemen gambar via Cloudinary
- Sinkronisasi data jalan nasional & lokal dari GeoJSON
- Analisis spasial fasilitas umum

## Status Kepemilikan

Status kepemilikan fasilitas di-inferensi otomatis berdasarkan nama:
- **Puskesmas** → Kecamatan
- **RSUD** → Kabupaten
- **SDN** (Sekolah Dasar Negeri) → Kabupaten
- Fasilitas lainnya → NULL (perlu input manual)

## Kontribusi

Untuk berkontribusi:
1. Fork repository
2. Buat branch fitur (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'Tambah fitur: ...'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request

## Support & Kontak

Untuk pertanyaan atau laporan bug, silakan hubungi tim development.
