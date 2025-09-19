from fastapi import APIRouter,Depends,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .import database,schemas,models,utils,oauth2

router=APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/",response_model=schemas.Token)
def user_login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    UL=db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not UL:
        raise HTTPException(status_code=401,detail="Invalid Username or Password")
    verify1=utils.verify(user_credential.password,UL.password)
    if not verify1:
        raise HTTPException(status_code=401,detail="Invalid username or password")
    access_token=oauth2.create_access_token(data={"user_id":UL.id})
    return {"access_token":access_token,"token_type":"bearer"}