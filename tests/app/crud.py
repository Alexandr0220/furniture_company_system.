from sqlalchemy.orm import Session
from app import models

def get_products(db: Session):
    return db.query(models.Product).all()

def get_workshops(db: Session):
    return db.query(models.Workshop).all()

def get_product_types(db: Session):
    return db.query(models.ProductType).all()

def get_materials(db: Session):
    return db.query(models.Material).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, article: str, name: str, min_price: float, product_type_id: int, material_id: int):
    obj = models.Product(
        article=article,
        name=name,
        min_price=min_price,
        product_type_id=product_type_id,
        material_id=material_id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_product(db: Session, product_id: int, article: str, name: str, min_price: float, product_type_id: int, material_id: int):
    obj = get_product(db, product_id)
    if not obj:
        return None
    obj.article = article
    obj.name = name
    obj.min_price = min_price
    obj.product_type_id = product_type_id
    obj.material_id = material_id
    db.commit()
    db.refresh(obj)
    return obj

def get_product_workshop_times(db: Session, product_id: int):
    rows = db.query(models.ProductWorkshop).filter(models.ProductWorkshop.product_id == product_id).all()
    return [r.time_min for r in rows]
