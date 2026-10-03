from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.security import ALGORITHM, get_secret_by_role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kredensial tidak valid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Dekode tanpa memverifikasi signature terlebih dahulu untuk mendapatkan id_role
        unverified_payload = jwt.get_unverified_claims(token)
        id_role = unverified_payload.get("id_role")
        
        if id_role is None:
            raise credentials_exception
            
        # Ambil secret yang benar sesuai rolenya
        secret_key = get_secret_by_role(id_role)
        
        # Dekode dan verifikasi dengan secret yang benar
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        
        id_user = payload.get("id_user")
        if id_user is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

def get_current_user_role(current_user: dict = Depends(get_current_user)):
    # id_role 1 for User
    if current_user.get("id_role") != 1:
        raise HTTPException(status_code=403, detail="Akses ditolak: Hanya user yang diizinkan")
    return current_user

def get_current_admin_kecamatan_role(current_user: dict = Depends(get_current_user)):
    # id_role 2 for Admin Kecamatan
    if current_user.get("id_role") != 2:
        raise HTTPException(status_code=403, detail="Akses ditolak: Hanya admin kecamatan yang diizinkan")
    return current_user

def get_current_admin_kabupaten_role(current_user: dict = Depends(get_current_user)):
    # id_role 3 for Admin Kabupaten
    if current_user.get("id_role") != 3:
        raise HTTPException(status_code=403, detail="Akses ditolak: Hanya admin kabupaten yang diizinkan")
    return current_user

def get_current_admin_role(current_user: dict = Depends(get_current_user)):
    # id_role 2 for Admin Kecamatan, 3 for Admin Kabupaten
    if current_user.get("id_role") not in [2, 3]:
        raise HTTPException(status_code=403, detail="Akses ditolak: Hanya admin yang diizinkan")
    return current_user
