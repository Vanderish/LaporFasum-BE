from fastapi import FastAPI
from app.api.routes import auth_route
from app.api.routes import user_route
from app.api.routes import admin_kecamatan_route
from app.api.routes import kategori_route
from app.api.routes import master_route
from app.api.routes import laporan_route
from app.api.routes import dashboard_route
from app.api.routes import peta_route
import cloudinary
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Sistem Pelaporan Fasilitas Umum")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://10.253.129.98:5174/",
    "https://98rp1d00-8000.asse.devtunnels.ms/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Konfigurasi Cloudinary bisa diletakkan saat aplikasi berjalan (on startup)
# atau di-load dari file core/config.py
cloudinary.config(
  cloud_name = "nama_cloud_kamu",
  api_key = "api_key_kamu",
  api_secret = "api_secret_kamu"
)

# Mendaftarkan router modular
# app.include_router(laporan_route.router)
app.include_router(auth_route.router)
app.include_router(user_route.router)
app.include_router(admin_kecamatan_route.router)
app.include_router(kategori_route.router)
app.include_router(master_route.router)
app.include_router(laporan_route.router)
app.include_router(dashboard_route.router)
app.include_router(peta_route.router)

@app.get("/")
def root():
    return {"message": "API Aktif! Buka /docs untuk dokumentasi Swagger UI"}