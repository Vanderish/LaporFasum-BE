import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

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
