from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    "https://localhost",
    "capacitor://localhost",
    "https://laporfasum.onrender.com",
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

# Global exception handler to ensure CORS headers on all error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Get the origin from request
    origin = request.headers.get("origin", "")
    # Only allow known origins
    allowed_origin = origin if origin in origins else (origins[0] if origins else "")
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers={
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Credentials": "true",
        }
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