import os
import hashlib
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import bcrypt

load_dotenv()

USER_SECRET = os.getenv("USER_SECRET", "default_user_secret")
ADMIN_KEC_SECRET = os.getenv("ADMIN_KEC_SECRET", "default_admin_kec_secret")
ADMIN_KAB_SECRET = os.getenv("ADMIN_KAB_SECRET", "default_admin_kab_secret")

def get_secret_by_role(id_role: int) -> str:
    if id_role == 1:
        return USER_SECRET
    elif id_role == 2:
        return ADMIN_KEC_SECRET
    elif id_role == 3:
        return ADMIN_KAB_SECRET
    else:
        raise ValueError("Invalid role ID")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 3

def verify_password(plain_password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    plain_password = plain_password[:72]
    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    password = password[:72]
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password, salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    id_role = to_encode.get("id_role")
    if id_role is None:
        raise ValueError("id_role is required to create access token")
    
    secret_key = get_secret_by_role(id_role)
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt
