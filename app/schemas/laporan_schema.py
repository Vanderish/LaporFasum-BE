from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LaporanCreate(BaseModel):
    judul_laporan: str
    deskripsi: str
    latitude: float
    longitude: float
    id_kategori: int
    id_kecamatan_kejadian: Optional[int] = None

class LaporanUpdateStatus(BaseModel):
    status_terkini: str
    kewenangan_penanganan: str
    tanggapan_admin: Optional[str] = None

class LaporanResponse(BaseModel):
    id_laporan: int
    judul_laporan: str
    deskripsi: str
    foto_bukti: Optional[str]
    latitude: float
    longitude: float
    status_terkini: str
    kewenangan_penanganan: Optional[str]
    id_kategori: int
    id_kecamatan_kejadian: int
    id_user: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class LaporanDetailResponse(LaporanResponse):
    nama_kategori: Optional[str] = None
    nama_kecamatan: Optional[str] = None
    nama_lengkap: Optional[str] = None

    class Config:
        from_attributes = True

class RiwayatStatusResponse(BaseModel):
    id_riwayat: int
    id_laporan: int
    status_sebelum: str
    status_sesudah: str
    kewenangan_penanganan: str
    tanggapan_admin: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardWargaResponse(BaseModel):
    statistik_personal: dict
    aktivitas_sekitar: List[dict]

class DashboardAdminResponse(BaseModel):
    statistik_status: dict
    rekapitulasi_kategori: List[dict]

class HeatmapResponse(BaseModel):
    latitude: List[float]
    longitude: List[float]