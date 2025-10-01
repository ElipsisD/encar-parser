from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = BASE_DIR.parent / "cars.db"
