from sqlalchemy.orm import Session
import models, schemas


def get_meme(db: Session, meme_id: int):
    return db.query(models.Meme).filter(models.Meme.id == meme_id).first()


def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def create_meme(db: Session, meme: schemas.MemeCreate):
    db_meme = models.Meme(**meme.model_dump())
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme_id: int, meme: schemas.MemeUpdate):
    db_meme = get_meme(db, meme_id)
    if db_meme is None:
        return None
    for key, value in meme.model_dump().items():
        setattr(db_meme, key, value)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def delete_meme(db: Session, meme_id: int):
    db_meme = get_meme(db, meme_id)
    if db_meme is None:
        return False
    db.delete(db_meme)
    db.commit()
    return True
