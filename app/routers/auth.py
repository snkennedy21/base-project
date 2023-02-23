from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..schemas import UserLogin
from ..models import User

from .. import database, utils

router = APIRouter(
  tags = ["Authentication"]
)

@router.post('/login')
def login(response: Response, user_credentials: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(User).where(User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Login Credentials"
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Login Credentials"
        )
    
    return {"token": "example token"}
    


