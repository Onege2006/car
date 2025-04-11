from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app import models
from app.database import engine, get_db
from app.routes import users, cars
from app.auth import get_current_user  # 🔐 Проверка токена

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(cars.router, prefix="/cars", tags=["Cars"])

app.mount("/static", StaticFiles(directory="static"), name="static")

# 🌐 Главная страница — с owner'ами
@app.get("/", response_class=HTMLResponse)
def root(request: Request, db: Session = Depends(get_db)):
    cars = db.query(models.Car).options(joinedload(models.Car.owner)).all()  # ← загружаем владельцев
    return templates.TemplateResponse("index.html", {"request": request, "cars": cars})

# 🚗 Добавление авто (ТОЛЬКО для залогиненных)
@app.post("/add")
def add_car(
    request: Request,
    title: str = Form(...),
    brand: str = Form(...),
    year: int = Form(...),
    description: str = Form(None),
    image_url: str = Form(...),
    db: Session = Depends(get_db)
):
    new_car = models.Car(
        title=title,
        brand=brand,
        year=year,
        description=description,
        image_url=image_url
    )

    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return RedirectResponse(url="/", status_code=303)

# 🔍 Галерея
@app.get("/gallery", response_class=HTMLResponse)
def show_gallery(request: Request, db: Session = Depends(get_db)):
    cars = db.query(models.Car).options(joinedload(models.Car.owner)).all()  # тоже с owner
    return templates.TemplateResponse("gallery.html", {"request": request, "cars": cars})
