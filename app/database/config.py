from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URLs
red_movilidad_url = "sqlite:///./sql_app_1.db"
dtpm_url = "sqlite:///./sql_app_2.db"

mob_red_engine = create_engine(red_movilidad_url)
dtpm_engine = create_engine(dtpm_url)

# Session Makers
SessionLocalRed = sessionmaker(autocommit=False, autoflush=False, bind=mob_red_engine)
SessionLocalDTPM = sessionmaker(autocommit=False, autoflush=False, bind=dtpm_engine)

Base = declarative_base()
