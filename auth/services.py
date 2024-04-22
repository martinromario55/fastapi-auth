from fastapi import HTTPException, status
from datetime import timedelta

from users.models import User
from core.security import verify_password, create_access_token, create_refresh_token, get_token_payload
from core.config import settings
from .responses import TokenResponse

async def get_token(data, db):
    user = db.query(User).filter(User.email == data.username).first()

    # Check if email exists in the database
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the password is correct
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Login Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Verify user
    _verify_user_access(user=user)
    
    # Return token
    return await _get_user_token(user=user) # Return access token and refresh token


def _verify_user_access(user: User):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unverified user. Please verify through email",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        
# Get token
async def _get_user_token(user: User, refresh_token=None):
    payload = {"id": user.id}
    
    # Create access token
    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(payload, access_token_expiry)
    
    if not refresh_token:
        # Create refresh token
        refresh_token = await create_refresh_token(payload)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )
    
async def get_refresh_token(token, db):
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return await _get_user_token(user=user, refresh_token=token)