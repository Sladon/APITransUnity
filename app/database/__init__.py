from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URLs
red_movilidad_url = "sqlite:///./sql_app_1.db"
dtpm_url = "sqlite:///./sql_app_2.db"

# Engines
engine_1 = create_engine(red_movilidad_url)
engine_2 = create_engine(dtpm_url)

# Session Makers
SessionLocal_1 = sessionmaker(autocommit=False, autoflush=False, bind=engine_1)
SessionLocal_2 = sessionmaker(autocommit=False, autoflush=False, bind=engine_2)

Base = declarative_base()

# Dependency getters for each DB


def get_red_db():
    db = SessionLocal_1()
    try:
        yield db
    finally:
        db.close()


def get_dtpm_db_():
    db = SessionLocal_2()
    try:
        yield db
    finally:
        db.close()
