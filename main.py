from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

load_dotenv()

app = FastAPI(title="Sistem Pelaporan Fasilitas Umum")

# CORS Configuration
# Origin tambahan bisa diisi lewat env ALLOWED_ORIGINS (dipisah koma), contoh:
# ALLOWED_ORIGINS=https://frontend-saya.up.railway.app,https://domain-produksi.com
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://192.168.11.69:5173",
    "http://localhost",
    "capacitor://localhost",
    "https://98rp1d00-8000.asse.devtunnels.ms",
]

extra_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

origins = list(dict.fromkeys(default_origins + extra_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/health")
def health():
    return {"status": "ok"}