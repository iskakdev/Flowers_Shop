from pydantic import BaseModel

class CategoryInputSchema(BaseModel):
    category: str


class CategoryOutputSchema(BaseModel):
    id: int
    category: str


class ProductInputSchema(BaseModel):
    product_name: str
    image: str
    price: int
    category_id: int


class ProductOutputSchema(BaseModel):
    id: int
    product_name: str
    image: str
    price: int
    category_id: int
