CREATE TABLE IF NOT EXISTS jalan_v2 (
  id_jalan INT AUTO_INCREMENT PRIMARY KEY,
  nama_jalan VARCHAR(200) NOT NULL,
  kategori_jalan VARCHAR(50) NOT NULL,
  status_kepemilikan ENUM('Nasional','Provinsi','Kabupaten','Kecamatan'),
  koordinat_lintasan LONGTEXT NOT NULL,
  properties JSON,
  id_kabupaten INT,
  id_kategori INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_kategori (kategori_jalan),
  INDEX idx_status (status_kepemilikan),
  INDEX idx_nama (nama_jalan)
);

-- Drop any existing unique constraints
ALTER TABLE jalan_v2 DROP INDEX IF EXISTS uk_jalan_kategori;
ALTER TABLE jalan_v2 DROP INDEX IF EXISTS nama_jalan;
ALTER TABLE jalan_v2 DROP INDEX IF EXISTS id_kategori;

-- Create composite index for pagination
CREATE INDEX idx_nama_kategori ON jalan_v2 (nama_jalan, kategori_jalan);
