from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/trees")
def read_trees(db: Session = Depends(get_db)):
    return db.query(models.Tree).all()

@app.post("/trees")
def save_new_tree(tree_input: dict, db: Session = Depends(get_db)):
    new_record = models.Tree(data=tree_input)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@app.put("/trees/{tree_id}")
def update_existing_tree(tree_id: int, tree_input: dict, db: Session = Depends(get_db)):
    db_tree = db.query(models.Tree).filter(models.Tree.id == tree_id).first()
    if not db_tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    
    db_tree.data = tree_input
    db.commit()
    db.refresh(db_tree)
    return db_tree