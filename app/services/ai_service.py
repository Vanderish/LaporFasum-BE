import os
import json
import httpx
from google import genai
from google.genai import types
from app.core.database import get_db_connection
from fastapi import HTTPException

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

MODEL_NAME = "gemini-3.1-flash-lite"

DEFAULT_KATEGORI_ID = 16

KATEGORI_LIST = [
    {"id_kategori": 1, "nama_kategori": "Jalan dan Jembatan"},
    {"id_kategori": 2, "nama_kategori": "Penerangan Jalan Umum (PJU)"},
    {"id_kategori": 3, "nama_kategori": "Saluran Air dan Drainase"},
    {"id_kategori": 4, "nama_kategori": "Pengelolaan Sampah dan Kebersihan"},
    {"id_kategori": 5, "nama_kategori": "Taman dan Ruang Terbuka Hijau (RTH)"},
    {"id_kategori": 6, "nama_kategori": "Fasilitas Kesehatan"},
    {"id_kategori": 7, "nama_kategori": "Fasilitas Pendidikan"},
    {"id_kategori": 8, "nama_kategori": "Rambu dan Marka Jalan"},
    {"id_kategori": 9, "nama_kategori": "Transportasi Publik (Halte, Terminal)"},
    {"id_kategori": 10, "nama_kategori": "Fasilitas Olahraga dan Rekreasi"},
    {"id_kategori": 11, "nama_kategori": "Pasar Tradisional"},
    {"id_kategori": 12, "nama_kategori": "Tempat Ibadah"},
    {"id_kategori": 13, "nama_kategori": "Fasilitas Pemerintahan dan Layanan Publik"},
    {"id_kategori": 14, "nama_kategori": "Fasilitas Keamanan dan Keselamatan (Polisi, Damkar)"},
    {"id_kategori": 15, "nama_kategori": "Pusat Perbelanjaan dan Fasilitas Ekonomi Modern"},
    {"id_kategori": 16, "nama_kategori": "Lainnya"},
]


def build_prompt(judul: str, deskripsi: str) -> str:
    kategori_str = "\n".join([f"- id_kategori: {k['id_kategori']}, nama_kategori: {k['nama_kategori']}" for k in KATEGORI_LIST])
    return f"""Anda adalah sistem klasifikasi otomatis laporan fasilitas umum untuk Kabupaten Lamongan.

Daftar kategori resmi yang tersedia:
{kategori_str}

Data laporan yang perlu diklasifikasikan:
Judul: {judul}
Deskripsi: {deskripsi}
Foto bukti: [disediakan sebagai gambar lampiran]

Tugas Anda:
1. Analisis **judul, deskripsi, DAN foto bukti** laporan secara menyeluruh.
2. Pilih **satu** kategori yang paling cocok dari daftar di atas berdasarkan analisis teks dan visual gambar.
3. Kembalikan **hanya** JSON valid dengan format berikut (tanpa markdown, tanpa penjelasan tambahan):
{{"id_kategori": <id_kategori_terpilih>}}

Jika tidak ada kategori yang cocok, pilih kategori yang paling mendekati."""


async def download_image(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=30.0) as http_client:
        resp = await http_client.get(url)
        resp.raise_for_status()
        return resp.content


async def klasifikasi_dan_teruskan_laporan(
    id_laporan: int,
    judul: str,
    deskripsi: str,
    foto_url: str,
    id_kecamatan: int
):
    if not client:
        print(f"[AI] GEMINI_API_KEY tidak tersedia, skip klasifikasi untuk laporan {id_laporan}")
        return

    try:
        prompt = build_prompt(judul, deskripsi)

        image_bytes = await download_image(foto_url)
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, image_part],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )

        result_text = response.text.strip()
        result = json.loads(result_text)
        id_kategori = result.get("id_kategori")

        valid_ids = {k["id_kategori"] for k in KATEGORI_LIST}
        if not id_kategori or not isinstance(id_kategori, int):
            print(f"[AI] Hasil klasifikasi tidak valid untuk laporan {id_laporan}: {result_text}")
            id_kategori = DEFAULT_KATEGORI_ID
        elif id_kategori not in valid_ids:
            print(f"[AI] ID kategori {id_kategori} tidak valid untuk laporan {id_laporan}, fallback ke default")
            id_kategori = DEFAULT_KATEGORI_ID

        db = get_db_connection()
        if not db:
            print(f"[AI] Koneksi DB gagal saat update kategori laporan {id_laporan}")
            return
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE laporan SET id_kategori = %s WHERE id_laporan = %s",
                (id_kategori, id_laporan)
            )
            db.commit()
            print(f"[AI] Laporan {id_laporan} dikategorikan ke id_kategori={id_kategori}")
        finally:
            cursor.close()
            db.close()

        await notify_admin_kecamatan(id_laporan, id_kecamatan, id_kategori)

    except json.JSONDecodeError as e:
        print(f"[AI] Gagal parse JSON dari Gemini untuk laporan {id_laporan}: {e}")
        await _update_kategori_default(id_laporan)
    except httpx.HTTPError as e:
        print(f"[AI] Gagal download gambar untuk laporan {id_laporan}: {e}")
        await _update_kategori_default(id_laporan)
    except Exception as e:
        print(f"[AI] Error tak terduga saat klasifikasi laporan {id_laporan}: {e}")
        await _update_kategori_default(id_laporan)


async def _update_kategori_default(id_laporan: int):
    db = get_db_connection()
    if not db:
        return
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE laporan SET id_kategori = %s WHERE id_laporan = %s",
            (DEFAULT_KATEGORI_ID, id_laporan)
        )
        db.commit()
        print(f"[AI] Laporan {id_laporan} dikategorikan ke default id_kategori={DEFAULT_KATEGORI_ID}")
    finally:
        cursor.close()
        db.close()


async def notify_admin_kecamatan(id_laporan: int, id_kecamatan: int, id_kategori: int):
    db = get_db_connection()
    if not db:
        return
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_user FROM users WHERE id_role = 2 AND id_kecamatan = %s",
            (id_kecamatan,)
        )
        admins = cursor.fetchall()
        if not admins:
            print(f"[Notif] Tidak ada admin kecamatan untuk id_kecamatan={id_kecamatan}")
            return

        cursor.execute(
            "SELECT nama_kategori FROM kategori_fasilitas WHERE id_kategori = %s",
            (id_kategori,)
        )
        kat = cursor.fetchone()
        nama_kategori = kat["nama_kategori"] if kat else "Tidak diketahui"

        for admin in admins:
            cursor.execute(
                """
                INSERT INTO notifikasi (id_user, id_laporan, judul, pesan, tipe_notifikasi)
                VALUES (%s, %s, %s, %s, 'laporan_baru')
                """,
                (
                    admin["id_user"],
                    id_laporan,
                    "Laporan Baru Masuk",
                    f"Laporan baru telah dikategorikan ke '{nama_kategori}' di wilayah Anda.",
                )
            )
        db.commit()
        print(f"[Notif] Dikirim ke {len(admins)} admin kecamatan untuk laporan {id_laporan}")
    finally:
        cursor.close()
        db.close()