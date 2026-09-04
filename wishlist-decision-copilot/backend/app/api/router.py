from fastapi import APIRouter
from app.api.endpoints import health, products, wishlist, decision, compare, analytics

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])
api_router.include_router(decision.router, prefix="/decision", tags=["decision"])
api_router.include_router(compare.router, prefix="/compare", tags=["compare"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
