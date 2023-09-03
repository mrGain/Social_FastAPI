from jose import JWSError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, models
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY: str = "8a8fc063aed20cb1f54e4198f75e05c89c354bc8149ecdc09368c0399567e46f"
ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
        return token_data
    except JWSError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Could not validate the credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter_by(id = token.id).first()
    return user