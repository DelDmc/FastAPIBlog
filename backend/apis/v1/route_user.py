from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.repository.user import create_new_user, retrieve_user

router = APIRouter()


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_in_db = retrieve_user(user.email, db=db)
    if user_in_db:
        raise HTTPException(detail=f"User with email {user.email} exists", status_code=status.HTTP_400_BAD_REQUEST)
    else:
      user = create_new_user(user=user, db=db)
      return user 