from typing import Tuple, Optional
from app.services import restaurant as restaurants_service
from fastapi import APIRouter
from app.services import analytics as analytics_service


router = APIRouter()


@router.get("/get-revenue-month/{restaurant_id}")
async def get_revenue_month(restaurant_id: str):
    revenue: Tuple[Optional[float], Optional[float]] = await analytics_service.get_revenue_by_month(restaurant_id)
    return {
        "currentMonth": revenue[0],
        "previousMonth": revenue[1]
    }


@router.get("/get-revenue-day/{restaurant_id}")
async def get_revenue_day(restaurant_id: str):
    revenue: Tuple[Optional[float], Optional[float]] = await analytics_service.get_revenue_by_day(restaurant_id)
    return {
        "today": revenue[0],
        "yesterday": revenue[1]
    }

@router.get("/get-order-count-month/{restaurant_id}")
async def get_order_count_month(restaurant_id: str):
    amount = await analytics_service.get_orders_count_by_month(restaurant_id)
    return {
        "currentMonth": amount[0],
        "previousMonth": amount[1]
    }


@router.get("/get-order-count-day/{restaurant_id}")
async def get_order_count_day(restaurant_id: str):
    amount = await analytics_service.get_orders_count_by_day(restaurant_id)
    return {
        "today": amount[0],
        "yesterday": amount[1]
    }

@router.get("/top-orders/{restaurant_id}")
async def most_ordered_items(restaurant_id: str):
    orders = await restaurants_service.most_ordered_last_seven_days(restaurant_id)
    return orders