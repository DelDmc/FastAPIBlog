from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.session import get_db
from core.hashing import Hasher
from core.config import settings
from db.repository.login import get_user_by_email
from core.security import create_access_token

router = APIRouter()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email=email, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db) # form_data.username == user.email
    if not user:
        raise HTTPException(
            detail="Incorrect email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token":access_token, "token_type":"bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Separate dependency to extract and validate token
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    """
    * jwt.decode() is used to decode the JWT passed in the token variable.
    * It takes the secret key and algorithm that was used to encode the JWT. These are fetched from the settings module.
    * Decoding the token validates the signature and structure of the JWT.
    * It returns a payload dictionary containing the claims in the token.
    * .get("sub") is retrieving the "sub" claim from the payload.
    * JWTs use the "sub" claim to store the subject identifier, which in this case is the user's email.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None: 
            raise InvalidTokenError()
    except JWTError:
        raise InvalidTokenError() from None
         
    return email

# Fetch user and raise explicit exception  
def get_current_user(email: str = Depends(get_user_from_token), db: Session = Depends(get_db)):
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise UserNotFoundError()
    return user 

# Exceptions
class InvalidTokenError(Exception):
    pass

class UserNotFoundError(Exception):
    pass