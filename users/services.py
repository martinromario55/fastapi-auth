from fastapi import status, HTTPException

from users.models import User
from core.security import get_password_hash

from datetime import datetime


async def create_user_account(data, db):
    user = db.query(User).filter(User.email == data.email).first()
    
    # Check if email exists in the database
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {data.email} already exists",
        )
        
    new_user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user