/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.18-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: pelaporan
-- ------------------------------------------------------
-- Server version	10.11.18-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `detail_fungsi_jalan`
--

DROP TABLE IF EXISTS `detail_fungsi_jalan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_fungsi_jalan` (
  `id_fungsi_jalan` int(11) NOT NULL AUTO_INCREMENT,
  `id_fasilitas_umum` int(11) NOT NULL,
  `nomor` varchar(50) DEFAULT NULL,
  `kode_prov` varchar(10) DEFAULT NULL,
  `kode_kota` varchar(10) DEFAULT NULL,
  `no_ruas` varchar(50) DEFAULT NULL,
  `kode_pkota` varchar(50) DEFAULT NULL,
  `nama_ruas` varchar(200) DEFAULT NULL,
  `panjang_jalan` varchar(50) DEFAULT NULL,
  `fungsi` varchar(100) DEFAULT NULL,
  `keterangan` varchar(200) DEFAULT NULL,
  `kelas_jln` varchar(50) DEFAULT NULL,
  `lhrt` varchar(100) DEFAULT NULL,
  `niaga` varchar(100) DEFAULT NULL,
  `lebar_m` varchar(100) DEFAULT NULL,
  `tipe_geometri` varchar(50) DEFAULT 'LineString',
  `bbox` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`bbox`)),
  `koordinat_lintasan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`koordinat_lintasan`)),
  PRIMARY KEY (`id_fungsi_jalan`),
  KEY `id_fasilitas_umum` (`id_fasilitas_umum`),
  CONSTRAINT `detail_fungsi_jalan_ibfk_1` FOREIGN KEY (`id_fasilitas_umum`) REFERENCES `fasilitas_umum` (`id_fasilitas_umum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4977 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detail_jalan_nasional`
--

DROP TABLE IF EXISTS `detail_jalan_nasional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_jalan_nasional` (
  `id_jalan_nasional` int(11) NOT NULL AUTO_INCREMENT,
  `id_fasilitas_umum` int(11) NOT NULL,
  `namobj` varchar(200) NOT NULL,
  `tipe_geometri` varchar(50) DEFAULT 'LineString',
  `bbox` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`bbox`)),
  `koordinat_lintasan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`koordinat_lintasan`)),
  PRIMARY KEY (`id_jalan_nasional`),
  KEY `id_fasilitas_umum` (`id_fasilitas_umum`),
  CONSTRAINT `detail_jalan_nasional_ibfk_1` FOREIGN KEY (`id_fasilitas_umum`) REFERENCES `fasilitas_umum` (`id_fasilitas_umum`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fasilitas_umum`
--

DROP TABLE IF EXISTS `fasilitas_umum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fasilitas_umum` (
  `id_fasilitas_umum` int(11) NOT NULL AUTO_INCREMENT,
  `id_kabupaten` int(11) NOT NULL,
  `nama_fasilitas` varchar(200) NOT NULL,
  `id_kategori` int(11) NOT NULL,
  `detail` text DEFAULT NULL,
  `status_kepemilikan` enum('Desa','Kecamatan','Kabupaten','Provinsi','Nasional') DEFAULT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `id_instansi` int(11) NOT NULL,
  PRIMARY KEY (`id_fasilitas_umum`),
  KEY `id_kabupaten` (`id_kabupaten`),
  KEY `fk_kategori_fasilitas` (`id_kategori`),
  KEY `fk_fasilitas_instansi` (`id_instansi`),
  CONSTRAINT `fasilitas_umum_ibfk_1` FOREIGN KEY (`id_kabupaten`) REFERENCES `kabupaten` (`id_kabupaten`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_fasilitas_instansi` FOREIGN KEY (`id_instansi`) REFERENCES `instansi_kewenangan` (`id_instansi`) ON UPDATE CASCADE,
  CONSTRAINT `fk_kategori_fasilitas` FOREIGN KEY (`id_kategori`) REFERENCES `kategori_fasilitas` (`id_kategori`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5579 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instansi_kewenangan`
--

DROP TABLE IF EXISTS `instansi_kewenangan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `instansi_kewenangan` (
  `id_instansi` int(11) NOT NULL AUTO_INCREMENT,
  `tingkat_kewenangan` varchar(50) NOT NULL,
  `nama_instansi` varchar(150) NOT NULL,
  `kontak_instansi` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_instansi`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kabupaten`
--

DROP TABLE IF EXISTS `kabupaten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `kabupaten` (
  `id_kabupaten` int(11) NOT NULL AUTO_INCREMENT,
  `nama_kabupaten` varchar(100) NOT NULL,
  `lat` decimal(10,8) DEFAULT NULL,
  `lng` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id_kabupaten`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kategori_fasilitas`
--

DROP TABLE IF EXISTS `kategori_fasilitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategori_fasilitas` (
  `id_kategori` int(11) NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(100) NOT NULL,
  PRIMARY KEY (`id_kategori`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kecamatan`
--

DROP TABLE IF EXISTS `kecamatan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `kecamatan` (
  `id_kecamatan` int(11) NOT NULL AUTO_INCREMENT,
  `id_kabupaten` int(11) NOT NULL,
  `nama_kecamatan` varchar(100) NOT NULL,
  `lat` decimal(10,8) DEFAULT NULL,
  `lng` decimal(11,8) DEFAULT NULL,
  PRIMARY KEY (`id_kecamatan`),
  KEY `id_kabupaten` (`id_kabupaten`),
  CONSTRAINT `kecamatan_ibfk_1` FOREIGN KEY (`id_kabupaten`) REFERENCES `kabupaten` (`id_kabupaten`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `laporan`
--

DROP TABLE IF EXISTS `laporan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `laporan` (
  `id_laporan` int(11) NOT NULL AUTO_INCREMENT,
  `id_pelapor` int(11) NOT NULL,
  `id_kategori` int(11) NOT NULL,
  `id_fasilitas_umum` int(11) DEFAULT NULL,
  `id_kecamatan_kejadian` int(11) NOT NULL,
  `judul_laporan` varchar(200) NOT NULL,
  `deskripsi_laporan` text NOT NULL,
  `foto_bukti` varchar(255) NOT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `kewenangan_penanganan` enum('Desa','Kecamatan','Kabupaten','Provinsi','Nasional') DEFAULT NULL,
  `status_terkini` enum('Menunggu Verifikasi','Diterima','Selesai') DEFAULT 'Menunggu Verifikasi',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_laporan`),
  KEY `id_pelapor` (`id_pelapor`),
  KEY `id_kategori` (`id_kategori`),
  KEY `id_fasilitas_umum` (`id_fasilitas_umum`),
  KEY `id_kecamatan_kejadian` (`id_kecamatan_kejadian`),
  CONSTRAINT `laporan_ibfk_1` FOREIGN KEY (`id_pelapor`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `laporan_ibfk_2` FOREIGN KEY (`id_kategori`) REFERENCES `kategori_fasilitas` (`id_kategori`) ON UPDATE CASCADE,
  CONSTRAINT `laporan_ibfk_3` FOREIGN KEY (`id_fasilitas_umum`) REFERENCES `fasilitas_umum` (`id_fasilitas_umum`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `laporan_ibfk_4` FOREIGN KEY (`id_kecamatan_kejadian`) REFERENCES `kecamatan` (`id_kecamatan`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifikasi`
--

DROP TABLE IF EXISTS `notifikasi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifikasi` (
  `id_notifikasi` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_laporan` int(11) DEFAULT NULL,
  `judul` varchar(150) NOT NULL,
  `pesan` text NOT NULL,
  `tipe_notifikasi` enum('status_laporan','tanggapan_admin','laporan_baru') NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_notifikasi`),
  KEY `id_user` (`id_user`),
  KEY `id_laporan` (`id_laporan`),
  CONSTRAINT `notifikasi_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `notifikasi_ibfk_2` FOREIGN KEY (`id_laporan`) REFERENCES `laporan` (`id_laporan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `riwayat_status_laporan`
--

DROP TABLE IF EXISTS `riwayat_status_laporan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `riwayat_status_laporan` (
  `id_riwayat` int(11) NOT NULL AUTO_INCREMENT,
  `id_laporan` int(11) NOT NULL,
  `id_admin_pemroses` int(11) NOT NULL,
  `status_update` enum('Menunggu Verifikasi','Diterima','Selesai') NOT NULL,
  `tanggapan_admin` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_riwayat`),
  KEY `id_laporan` (`id_laporan`),
  KEY `id_admin_pemroses` (`id_admin_pemroses`),
  CONSTRAINT `riwayat_status_laporan_ibfk_1` FOREIGN KEY (`id_laporan`) REFERENCES `laporan` (`id_laporan`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `riwayat_status_laporan_ibfk_2` FOREIGN KEY (`id_admin_pemroses`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_role` int(11) NOT NULL AUTO_INCREMENT,
  `nama_role` varchar(50) NOT NULL,
  PRIMARY KEY (`id_role`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `nik` char(16) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(150) NOT NULL,
  `alamat_domisili` text NOT NULL,
  `id_role` int(11) NOT NULL,
  `id_kecamatan` int(11) DEFAULT NULL,
  `id_kabupaten` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `nik` (`nik`),
  UNIQUE KEY `email` (`email`),
  KEY `id_role` (`id_role`),
  KEY `id_kecamatan` (`id_kecamatan`),
  KEY `id_kabupaten` (`id_kabupaten`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`) ON UPDATE CASCADE,
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`id_kecamatan`) REFERENCES `kecamatan` (`id_kecamatan`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `users_ibfk_3` FOREIGN KEY (`id_kabupaten`) REFERENCES `kabupaten` (`id_kabupaten`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-07 17:01:01
