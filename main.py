from fastapi import FastAPI
from flowers_shop.api import (flower_categories, flower_products)
import uvicorn

flowers_shop_app = FastAPI(title="Flowers Shop")

flowers_shop_app.include_router(flower_categories.category_router)
flowers_shop_app.include_router(flower_products.product_router)


if __name__ == "__main__":
    uvicorn.run("main:flowers_shop_app", host="127.0.0.1", port=8001, reload=True)
