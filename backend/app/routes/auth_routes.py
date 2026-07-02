from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import Register, Login
from ..hashing import hash_password
from ..hashing import verify_password
from ..auth import create_access_token
from ..dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter()


# Register
@router.post("/register")
def register(
        user: Register,
        db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(

        full_name=user.full_name,

        email=user.email,

        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "Registration Successful"
    }


# Login
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):  

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Dashboard
@router.get("/dashboard")
def dashboard(
        current_user=Depends(get_current_user)
):

    return {

        "message": f"Welcome {current_user}"
    }


# Logout
@router.post("/logout")
def logout():

    return {

        "message": "Logout Successful. Delete token from frontend."
    }
    
    
    # 65b1d796ab1571988be4f00a1fa5c0df120f4111d3f6a3470ad21cc4061d9962