import os
import pandas as pd
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models

IMPORT_DIR = "data/import"

def ensure_seed_data(db: Session):
    # minimal seed so UI works even without Excel
    if db.query(models.ProductType).count() == 0:
        db.add_all([models.ProductType(name="Классическая мебель"), models.ProductType(name="Современная мебель")])
    if db.query(models.Material).count() == 0:
        db.add_all([
            models.Material(name="Дуб", loss_percent=2.5),
            models.Material(name="МДФ", loss_percent=8.0)
        ])
    if db.query(models.Workshop).count() == 0:
        db.add_all([
            models.Workshop(name="Распил", workers_count=3, time_min=20),
            models.Workshop(name="Сборка", workers_count=5, time_min=40),
            models.Workshop(name="Покраска", workers_count=2, time_min=30),
        ])
    db.commit()

def import_excel_if_present(db: Session):
    # Optional: if *_import.xlsx exists, try to import known sheets.
    if not os.path.isdir(IMPORT_DIR):
        return
    files = [f for f in os.listdir(IMPORT_DIR) if f.endswith(".xlsx")]
    if not files:
        return

    # Very tolerant importer: looks for columns by keywords.
    for filename in files:
        path = os.path.join(IMPORT_DIR, filename)
        try:
            xl = pd.ExcelFile(path)
        except Exception:
            continue

        for sheet in xl.sheet_names:
            try:
                df = xl.parse(sheet)
            except Exception:
                continue

            cols = {c.lower(): c for c in df.columns}
            # crude mapping: if it has 'цех' => workshops, if has 'материал' => materials, if has 'продукт' => products
            lower_sheet = sheet.lower()
            if "цех" in lower_sheet:
                for _, row in df.iterrows():
                    name = str(row.get(cols.get("название", ""), "")).strip()
                    if not name:
                        continue
                    workers = int(row.get(cols.get("количество человек", cols.get("работников", "")), 0) or 0)
                    t = int(row.get(cols.get("время", cols.get("time", "")), 0) or 0)
                    db.add(models.Workshop(name=name, workers_count=workers, time_min=t))
            elif "материал" in lower_sheet:
                for _, row in df.iterrows():
                    name = str(row.get(cols.get("наименование", cols.get("название", "")), "")).strip()
                    if not name:
                        continue
                    loss = float(row.get(cols.get("потери", cols.get("loss_percent", "")), 0) or 0)
                    db.add(models.Material(name=name, loss_percent=loss))
            elif "тип" in lower_sheet:
                for _, row in df.iterrows():
                    name = str(row.get(cols.get("наименование", cols.get("название", "")), "")).strip()
                    if not name:
                        continue
                    db.add(models.ProductType(name=name))
            elif "продукт" in lower_sheet or "product" in lower_sheet:
                # requires existing type/material ids; we just attach first ones if missing
                pt = db.query(models.ProductType).first()
                mat = db.query(models.Material).first()
                for _, row in df.iterrows():
                    name = str(row.get(cols.get("наименование", cols.get("название", "")), "")).strip()
                    if not name:
                        continue
                    article = str(row.get(cols.get("артикул", cols.get("article", "")), "")).strip() or None
                    price = float(row.get(cols.get("минимальная стоимость", cols.get("min_price", "")), 0) or 0)
                    db.add(models.Product(
                        article=article,
                        name=name,
                        min_price=price,
                        product_type_id=pt.id if pt else 1,
                        material_id=mat.id if mat else 1
                    ))
        db.commit()

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_seed_data(db)
        import_excel_if_present(db)
        print("OK: база создана / данные (если были) импортированы.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
