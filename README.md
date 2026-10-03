# Sistem Pelaporan Fasilitas Umum Kabupaten Lamongan

Platform digital untuk pelaporan, monitoring, dan pengelolaan fasilitas umum di Kabupaten Lamongan. Sistem ini mengintegrasikan data pemetaan, infrastruktur jalan dari GeoJSON, serta memfasilitasi pelaporan berbasis komunitas dengan sistem verifikasi multi-level.

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
Dokumentasi API tersedia di: `http://localhost:8000/docs`

## Struktur Direktori

```
projek2/
├── app/
│   ├── core/           # Konfigurasi inti (database, security)
│   ├── models/         # Model database
│   ├── schemas/        # Pydantic schemas
│   ├── api/            # Endpoint API
│   └── services/       # Business logic
├── main.py             # Entry point aplikasi
├── seeder_jalan.py     # Script sinkronisasi data jalan
├── .env.example        # Template environment variables
├── requirements.txt    # Dependencies Python
└── pelaporan.sql       # Database dump
```

## Tech Stack

- **Backend**: FastAPI
- **Database**: MariaDB/MySQL
- **ORM/Connector**: mysql-connector-python
- **Authentication**: JWT
- **API Integration**: Gemini
- **Data Format**: GeoJSON

## User Roles

1. **User**: Dapat membuat dan melihat laporan pribadi
2. **Admin Kecamatan**: Verifikasi dan tanggapi laporan di tingkat kecamatan
3. **Admin Kabupaten**: Monitoring keseluruhan dan pelaporan kabupaten

## Fitur Utama

- Dashboard monitoring fasilitas publik
- Sistem pelaporan kerusakan/keluhan terukur
- Verifikasi multi-level oleh admin
- Integrasi pemetaan berbasis GIS
- Tracking riwayat status laporan
- Notifikasi real-time

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
