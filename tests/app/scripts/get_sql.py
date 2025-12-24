import sqlite3
import os

DB_PATH = "app/database/furniture.db"
OUT_PATH = "app/database/db_sql.sql"

def main():
    if not os.path.exists(DB_PATH):
        print("DB not found. Run: python -m app.scripts.import_data")
        return
    con = sqlite3.connect(DB_PATH)
    try:
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            for line in con.iterdump():
                f.write(f"{line}\n")
        print(f"OK: SQL-скрипт сохранен: {OUT_PATH}")
    finally:
        con.close()

if __name__ == "__main__":
    main()
