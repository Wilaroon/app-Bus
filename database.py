import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker





# Datos de conexión a RDS MySQL
load_dotenv()
db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_hosting = os.getenv("DB_HOST")
name_db = os.getenv("DB_NAME")

# URL de conexión para SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{db_username}:{db_password}@{db_hosting}/{name_db}"

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
