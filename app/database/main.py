from .config import SessionLocalRed, SessionLocalDTPM

def get_red_db():
    db = SessionLocalRed()
    try:
        yield db
    finally:
        db.close()


def get_dtpm_db():
    db = SessionLocalDTPM()
    try:
        yield db
    finally:
        db.close()
