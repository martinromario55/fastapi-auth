from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from core.database import get_db
from users.shemas import CreateUserRequest
from users.services import create_user_account

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


# Create User
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data=data, db=db)
    payload = {"message": "User account has been successfully created."}
    return JSONResponse(content=payload)