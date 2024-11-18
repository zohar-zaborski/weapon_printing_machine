from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError
from .. import crud, schemas, auth_utils
from ..database import get_db

router = APIRouter()

# OAuth2 scheme for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    return crud.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint to authenticate and log in a user, returning an access token.
    """
    # Fetch the user by username
    user = crud.get_user_by_username(db, username=form_data.username)
    
    if not user:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the password
   
    if not auth_utils.verify_password(form_data.password, user.password):
       
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token = auth_utils.create_access_token(data={"user_id": user.id, "sub": user.username})
   
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth_utils.decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve the current authenticated user's details.
    """
    payload = auth_utils.decode_access_token(token)
    username = payload.get("sub")
    user_id = payload.get("user_id")

    if not username or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
