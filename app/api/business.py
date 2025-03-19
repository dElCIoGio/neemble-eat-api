from fastapi import APIRouter
from app.schemas import restaurant as restaurant_schema

router = APIRouter()


@router.post("/set-restaurant")
async def set_up_restaurant(restaurant: restaurant_schema.RestaurantNew):
    print(restaurant)
    return True
