from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, crud, schemas
from typing import List

# Инициализация приложения
app = FastAPI()

# Создание базы данных
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/memes", response_model=List[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memes = crud.get_memes(db, skip=skip, limit=limit)
    return memes


@app.get("/memes/{meme_id}", response_model=schemas.Meme)
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id=meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@app.post("/memes", response_model=schemas.Meme)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.create_meme(db=db, meme=meme)


@app.put("/memes/{meme_id}", response_model=schemas.Meme)
def update_meme(meme_id: int, meme: schemas.MemeUpdate, db: Session = Depends(get_db)):
    db_meme = crud.update_meme(db=db, meme_id=meme_id, meme=meme)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@app.delete("/memes/{meme_id}")
def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    success = crud.delete_meme(db=db, meme_id=meme_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meme not found")
    return {"detail": "Meme deleted"}
