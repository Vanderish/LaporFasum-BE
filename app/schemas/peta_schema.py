from pydantic import BaseModel
from typing import Optional, List, Any

class GeojsonGeometry(BaseModel):
    type: str
    coordinates: Any

class GeojsonProperties(BaseModel):
    nama_jalan: Optional[str] = None
    kepemilikan: Optional[str] = None
    id_fasilitas: Optional[int] = None
    id_laporan: Optional[int] = None
    judul_laporan: Optional[str] = None
    status_terkini: Optional[str] = None
    kategori: Optional[str] = None

class GeojsonFeature(BaseModel):
    type: str = "Feature"
    geometry: GeojsonGeometry
    properties: GeojsonProperties

class GeojsonFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeojsonFeature]

class InfrastrukturFilter(BaseModel):
    kepemilikan: Optional[str] = None