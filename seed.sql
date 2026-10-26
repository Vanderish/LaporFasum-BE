-- Seed data referensi minimum untuk Sistem Pelaporan Fasilitas Umum Kabupaten Lamongan.
-- Jalankan SETELAH meng-import pelaporan.sql (skema).
-- Jalankan di database yang sama dengan aplikasi (Railway: MYSQLDATABASE, default "railway").
--
-- Cara pakai via Railway CLI:
--   railway connect MySQL
--   mysql> SOURCE seed.sql;
--
-- Idempotent: aman dijalankan berulang (INSERT IGNORE + id eksplisit).

SET NAMES utf8mb4;

-- ---------------------------------------------------------------------------
-- Kabupaten
-- ---------------------------------------------------------------------------
INSERT IGNORE INTO `kabupaten` (`id_kabupaten`, `nama_kabupaten`, `lat`, `lng`) VALUES
  (1, 'Lamongan', -7.11666670, 112.41666670);

-- ---------------------------------------------------------------------------
-- Kecamatan (27 kecamatan di Kabupaten Lamongan)
-- ---------------------------------------------------------------------------
INSERT IGNORE INTO `kecamatan` (`id_kecamatan`, `id_kabupaten`, `nama_kecamatan`) VALUES
  (1,  1, 'Babat'),
  (2,  1, 'Bluluk'),
  (3,  1, 'Brondong'),
  (4,  1, 'Deket'),
  (5,  1, 'Glagah'),
  (6,  1, 'Kalitengah'),
  (7,  1, 'Karangbinangun'),
  (8,  1, 'Karanggeneng'),
  (9,  1, 'Kedungpring'),
  (10, 1, 'Kembangbahu'),
  (11, 1, 'Lamongan'),
  (12, 1, 'Laren'),
  (13, 1, 'Maduran'),
  (14, 1, 'Mantup'),
  (15, 1, 'Modo'),
  (16, 1, 'Ngimbang'),
  (17, 1, 'Paciran'),
  (18, 1, 'Pucuk'),
  (19, 1, 'Sambeng'),
  (20, 1, 'Sarirejo'),
  (21, 1, 'Sekaran'),
  (22, 1, 'Solokuro'),
  (23, 1, 'Sugio'),
  (24, 1, 'Sukodadi'),
  (25, 1, 'Sukorame'),
  (26, 1, 'Tikung'),
  (27, 1, 'Turi');

-- ---------------------------------------------------------------------------
-- Roles
-- ---------------------------------------------------------------------------
INSERT IGNORE INTO `roles` (`id_role`, `nama_role`) VALUES
  (1, 'User'),
  (2, 'Admin Kecamatan'),
  (3, 'Admin Kabupaten');

-- ---------------------------------------------------------------------------
-- Kategori fasilitas (harus sama dengan KATEGORI_LIST di app/services/ai_service.py)
-- ---------------------------------------------------------------------------
INSERT IGNORE INTO `kategori_fasilitas` (`id_kategori`, `nama_kategori`) VALUES
  (1,  'Jalan dan Jembatan'),
  (2,  'Penerangan Jalan Umum (PJU)'),
  (3,  'Saluran Air dan Drainase'),
  (4,  'Pengelolaan Sampah dan Kebersihan'),
  (5,  'Taman dan Ruang Terbuka Hijau (RTH)'),
  (6,  'Fasilitas Kesehatan'),
  (7,  'Fasilitas Pendidikan'),
  (8,  'Rambu dan Marka Jalan'),
  (9,  'Transportasi Publik (Halte, Terminal)'),
  (10, 'Fasilitas Olahraga dan Rekreasi'),
  (11, 'Pasar Tradisional'),
  (12, 'Tempat Ibadah'),
  (13, 'Fasilitas Pemerintahan dan Layanan Publik'),
  (14, 'Fasilitas Keamanan dan Keselamatan (Polisi, Damkar)'),
  (15, 'Pusat Perbelanjaan dan Fasilitas Ekonomi Modern'),
  (16, 'Lainnya');

-- ---------------------------------------------------------------------------
-- Instansi kewenangan (CONTOH - sesuaikan dengan data instansi asli Anda).
-- Diperlukan karena fasilitas_umum.id_instansi NOT NULL (FK ke tabel ini).
-- ---------------------------------------------------------------------------
INSERT IGNORE INTO `instansi_kewenangan` (`id_instansi`, `tingkat_kewenangan`, `nama_instansi`) VALUES
  (1,  'Desa',      'Pemerintah Desa'),
  (2,  'Kecamatan', 'Pemerintah Kecamatan'),
  (3,  'Kabupaten', 'Dinas Pekerjaan Umum dan Penataan Ruang'),
  (4,  'Provinsi',  'Dinas Bina Marga Provinsi Jawa Timur'),
  (5,  'Nasional',  'Kementerian Pekerjaan Umum dan Perumahan Rakyat');
