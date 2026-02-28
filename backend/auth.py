from passlib.context import CryptContext
import uuid



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # truncate to 72 characters (bytes)
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password[:72])




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_fingerprint_id():
    return str(uuid.uuid4())

def generate_qr_id():
    return str(uuid.uuid4())