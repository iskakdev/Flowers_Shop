from fastapi import APIRouter, Depends, HTTPException
from flowers_shop.database.models import Category
from flowers_shop.database.schema import CategoryInputSchema, CategoryOutputSchema
from flowers_shop.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

category_router = APIRouter(prefix='/categories', tags=['Categories'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/', response_model=CategoryOutputSchema)
async def create_category(category: CategoryInputSchema, db: Session = Depends(get_db)):
    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get('/', response_model=List[CategoryOutputSchema])
async def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@category_router.get('/{category_id}', response_model=CategoryOutputSchema)
async def detail_categories(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.put('/{category_id}/', response_model=dict)
async def update_category(category_id: int, category: CategoryInputSchema,
                         db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for category_key, category_value in category.dict().items():
            setattr(category_db, category_key, category_value)

    db.commit()
    db.refresh(category_db)
    return {'massage': 'Category updated successfully'}


@category_router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}
