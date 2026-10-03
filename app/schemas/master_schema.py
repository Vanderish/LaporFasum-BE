from pydantic import BaseModel
from typing import Optional, List

class KecamatanResponse(BaseModel):
    id_kecamatan: int
    nama_kecamatan: str

    class Config:
        from_attributes = True

class KategoriResponse(BaseModel):
    id_kategori: int
    nama_kategori: str

    class Config:
        from_attributes = True

class FasilitasUmumQuery(BaseModel):
    nama: Optional[str] = None
    kategori: Optional[int] = None

class FasilitasUmumResponse(BaseModel):
    id_fasilitas: int
    nama_fasilitas: str
    id_kategori: int
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class KoordinatRute(BaseModel):
    latitude: float
    longitude: float

class RuteResponse(BaseModel):
    id_fasilitas: int
    nama_fasilitas: str
    koordinat: List[KoordinatRute]

    class Config:
        from_attributes = True