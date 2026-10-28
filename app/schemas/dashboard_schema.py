from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DashboardWargaResponse(BaseModel):
    statistik_wilayah: dict
    statistik_harian: List[dict]
    statistik_mingguan: List[dict]
    statistik_bulanan: List[dict]
    laporan_terbaru: List[dict]

class DashboardAdminResponse(BaseModel):
    status: str
    data: dict

class HeatmapResponse(BaseModel):
    latitude: List[float]
    longitude: List[float]