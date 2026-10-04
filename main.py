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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "nama_cloud_kamu"),
  api_key = os.getenv("CLOUDINARY_API_KEY", "api_key_kamu"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET", "api_secret_kamu")
)

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