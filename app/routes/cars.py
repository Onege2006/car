from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, database, crud, auth

router = APIRouter()


# 🟢 Получить список всех машин
@router.get("/", response_model=List[schemas.CarOut])
def get_cars(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_all_cars(db, skip, limit)


# 🟢 Получить одну машину по id
@router.get("/{car_id}", response_model=schemas.CarOut)
def get_car(car_id: int, db: Session = Depends(database.get_db)):
    car = crud.get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


# 🔒 Добавить машину (только авторизованным)
@router.post("/", response_model=schemas.CarOut)
def create_car(
    car: schemas.CarCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_car(db, car, user_id=current_user.id)


# 🔒 Удалить свою машину
@router.delete("/{car_id}")
def delete_car(
    car_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    car = crud.delete_car(db, car_id, user_id=current_user.id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found or not yours")
    return {"message": "Car deleted successfully"}

from fastapi import File, UploadFile
import os
import uuid

UPLOAD_FOLDER = "static"

@router.post("/upload")
def upload_image(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    if ext.lower() not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Only JPG/PNG images allowed")

    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    url = f"/static/{filename}"
    return {"image_url": url}
