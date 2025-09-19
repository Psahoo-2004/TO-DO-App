from fastapi import APIRouter,Depends,HTTPException,Query
from .. import models,schemas,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import hashed
from typing import Optional,List


router=APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)

@router.post("/",response_model=schemas.ToDoOut)
def create_task(task:schemas.ToDo,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    if db.query(models.TODO).filter(models.TODO.title == task.title,models.TODO.owner_id == current_user.id).first():
        raise HTTPException(status_code=400,detail="Task already added")
    CT=models.TODO(owner_id=current_user.id,**task.model_dump())
    db.add(CT)
    db.commit()
    db.refresh(CT)
    return CT

@router.get("/",response_model=List[schemas.ToDoOut])
def get_tasks(completed: Optional[bool] = Query(None, description="Filter tasks by completion status"),db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    GT=db.query(models.TODO).filter(models.TODO.owner_id == current_user.id)
    if completed is not None:  # Only filter if param is given
        GT = GT.filter(models.TODO.completed == completed)
    tasks=GT.all()
    return GT

@router.get("/{id}",response_model=schemas.ToDoOut)
def get_task_by_id(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    GTI=db.query(models.TODO).filter(models.TODO.id == id).first()
    if not GTI:
        raise HTTPException(status_code=404,detail="Does not Exists")
    if GTI.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized")
    return GTI

@router.put("/{id}",response_model=schemas.ToDoOut)
def update_status(id:int,task:schemas.UpdateToDO,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    US=db.query(models.TODO).filter(models.TODO.id == id).first()
    if not US:
        raise HTTPException(status_code=404,detail="Task not added")
    if US.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized")
    for key,value in task.model_dump().items():
        setattr(US,key,value)
    db.commit()
    return US

@router.delete("/{id}",response_model=schemas.ToDoOut)
def delete_task(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    DT=db.query(models.TODO).filter(models.TODO.id == id).first()
    if not DT:
        raise HTTPException(status_code=404,detail="Task not added")
    if DT.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Not Authorized")
    db.delete(DT)
    db.commit()
    return DT
