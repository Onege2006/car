from sqlalchemy.orm import Session
from app import models, schemas


def create_car(db: Session, car: schemas.CarCreate, user_id: int):
    new_car = models.Car(**car.dict(), owner_id=user_id)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

def get_all_cars(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Car).offset(skip).limit(limit).all()

def get_car_by_id(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()

def delete_car(db: Session, car_id: int, user_id: int):
    car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.owner_id == user_id).first()
    if car:
        db.delete(car)
        db.commit()
    return car
