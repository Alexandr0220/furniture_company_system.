from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models, crud, logic

app = FastAPI(title="Furniture Company System (Week 1)")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def db_session() -> Session:
    return SessionLocal()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    db = db_session()
    try:
        products = crud.get_products(db)
        result = []
        for p in products:
            times = crud.get_product_workshop_times(db, p.id)
            p.production_time = logic.calculate_production_time(times)
            result.append(p)
        return templates.TemplateResponse("products.html", {"request": request, "products": result})
    finally:
        db.close()

@app.get("/products/new", response_class=HTMLResponse)
def new_product(request: Request):
    db = db_session()
    try:
        return templates.TemplateResponse("product_form.html", {
            "request": request,
            "title": "Добавление продукции",
            "product": None,
            "product_types": crud.get_product_types(db),
            "materials": crud.get_materials(db),
            "error": None
        })
    finally:
        db.close()

@app.post("/products/new")
def create_product(
    article: str = Form(""),
    product_type_id: int = Form(...),
    name: str = Form(...),
    min_price: float = Form(...),
    material_id: int = Form(...)
):
    db = db_session()
    try:
        if min_price < 0:
            return templates.TemplateResponse("product_form.html", {
                "request": Request(scope={"type":"http"}),
                "title": "Добавление продукции",
                "product": None,
                "product_types": crud.get_product_types(db),
                "materials": crud.get_materials(db),
                "error": "Цена не может быть отрицательной."
            })
        crud.create_product(db, article, name, min_price, product_type_id, material_id)
        return RedirectResponse(url="/products", status_code=303)
    finally:
        db.close()

@app.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product(request: Request, product_id: int):
    db = db_session()
    try:
        product = crud.get_product(db, product_id)
        return templates.TemplateResponse("product_form.html", {
            "request": request,
            "title": "Редактирование продукции",
            "product": product,
            "product_types": crud.get_product_types(db),
            "materials": crud.get_materials(db),
            "error": None
        })
    finally:
        db.close()

@app.post("/products/{product_id}/edit")
def save_product(
    product_id: int,
    article: str = Form(""),
    product_type_id: int = Form(...),
    name: str = Form(...),
    min_price: float = Form(...),
    material_id: int = Form(...)
):
    db = db_session()
    try:
        if min_price < 0:
            product = crud.get_product(db, product_id)
            return templates.TemplateResponse("product_form.html", {
                "request": Request(scope={"type":"http"}),
                "title": "Редактирование продукции",
                "product": product,
                "product_types": crud.get_product_types(db),
                "materials": crud.get_materials(db),
                "error": "Цена не может быть отрицательной."
            })
        crud.update_product(db, product_id, article, name, min_price, product_type_id, material_id)
        return RedirectResponse(url="/products", status_code=303)
    finally:
        db.close()

@app.get("/workshops", response_class=HTMLResponse)
def workshops(request: Request):
    db = db_session()
    try:
        return templates.TemplateResponse("workshops.html", {"request": request, "workshops": crud.get_workshops(db)})
    finally:
        db.close()
