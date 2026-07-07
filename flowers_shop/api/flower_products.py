from fastapi import APIRouter, Depends, HTTPException
from flowers_shop.database.models import Product
from flowers_shop.database.schema import ProductInputSchema, ProductOutputSchema
from flowers_shop.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

product_router = APIRouter(prefix='/products', tags=['Products'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/', response_model=ProductOutputSchema)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/', response_model=List[ProductOutputSchema])
async def list_product(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products



@product_router.get('/{product_id}/', response_model=ProductInputSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Product not found', status_code=400)
    return product_db


@product_router.put('/{product_id}/', response_model=dict)
async def update_booking(product_id: int, product: ProductInputSchema,
                         db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Product not found', status_code=400)

    for product_key, product_value in product.dict().items():
            setattr(product_db, product_key, product_value)

    db.commit()
    db.refresh(product_db)
    return {'massage': 'Product updated successfully'}


@product_router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(detail='Product not found', status_code=400)
    db.delete(db_product)
    db.commit()
    return {'massage': 'Product deleted successfully'}
