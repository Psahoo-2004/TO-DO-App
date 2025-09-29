from fastapi import APIRouter,Depends,HTTPException
from .. import models,schemas,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import hashed

router=APIRouter(
    prefix="/users",
    tags=["User"]
)

# C
@router.post("/",response_model=schemas.UserOut)
def create_user(users:schemas.CreateUser,db:Session=Depends(get_db)):
    checkuser=db.query(models.User).filter(models.User.email == users.email).first()
    if checkuser:
        raise HTTPException(status_code=400,detail="Email already exists")
    hashed_password=hashed(users.password)
    users.password=hashed_password
    CU=models.User(**users.model_dump())
    db.add(CU)
    db.commit()
    db.refresh(CU)
    return CU

# R
# @router.get("/",response_model=list[schemas.UserOut])
# def get_user(db:Session=Depends(get_db),curent_user=Depends(oauth2.get_current_user)):
#     GU=db.query(models.User).all()
#     return GU

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    GUI=db.query(models.User).filter(models.User.id == current_user.id).first()
    if not GUI:
        raise HTTPException(status_code=404,detail="user doesnot exists")
    return GUI

# U
@router.put("/{id}",response_model=schemas.UserOut)
def update_user(users:schemas.UpdateUser,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    UU=db.query(models.User).filter(models.User.id == current_user.id).first()
    if not UU:
        raise HTTPException(status_code=404,detail="user doesnot exists")
    update_data = users.model_dump(exclude_unset=True)
    if "password" in update_data:
        if update_data["password"] == UU.password:
            raise HTTPException(status_code=400, detail="Please use a different password")
        # Hash the password
        update_data["password"] = hashed(update_data["password"])
    
    for key, value in update_data.items():
        setattr(UU, key, value)
    db.commit()
    return UU
# D
@router.delete("/{id}",response_model=schemas.UserOut)
def delete_user(db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    DU=db.query(models.User).filter(models.User.id == current_user.id).first()
    if not DU:
        raise HTTPException(status_code=404,detail="user doesnot exists")
    db.delete(DU)
    db.commit()
    return DU