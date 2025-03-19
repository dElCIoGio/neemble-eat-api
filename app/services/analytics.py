from typing import List, Tuple, Optional
from app.utils import utils
from google.cloud.firestore_v1 import DocumentReference

from app.crud import restaurant as restaurant_crud
from app.crud import order as order_crud


async def get_revenue_by_month(restaurant_id: str) -> Tuple[Optional[float], Optional[float]]:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if not restaurant_ref:
        return None, None

    restaurant_data = restaurant_ref.get().to_dict()
    total_revenue_current_month = 0
    total_revenue_last_month = 0
    if "orders" in restaurant_data:
        # Assume orders_refs are fetched correctly as a list of DocumentReferences
        orders_refs: List[DocumentReference] = restaurant_data["orders"]

        # Filter orders for the current month
        current_month_orders = utils.get_documents_created_this_month(orders_refs)
        for order_ref in current_month_orders:
            total = await get_order_total(order_ref.id)
            if total:
                total_revenue_current_month += total

        # Filter orders for the previous month
        last_month_orders = utils.get_documents_created_last_month(orders_refs)
        for order_ref in last_month_orders:
            total = await get_order_total(order_ref.id)
            if total:
                total_revenue_last_month += total

    return total_revenue_current_month, total_revenue_last_month


async def get_revenue_by_day(restaurant_id: str) -> Tuple[Optional[int], Optional[float]]:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if not restaurant_ref:
        return None, None

    restaurant_data = restaurant_ref.get().to_dict()
    total_revenue_today= 0
    total_revenue_yesterday = 0
    if "orders" in restaurant_data:
        # Assume orders_refs are fetched correctly as a list of DocumentReferences
        orders_refs: List[DocumentReference] = restaurant_data["orders"]

        # Filter orders for the current month
        current_month_orders = utils.get_documents_created_today(orders_refs)
        for order_ref in current_month_orders:
            total = await get_order_total(order_ref.id)
            if total:
                total_revenue_today += total

        # Filter orders for the previous month
        last_month_orders = utils.get_documents_created_yesterday(orders_refs)
        for order_ref in last_month_orders:
            total = await get_order_total(order_ref.id)
            if total:
                total_revenue_yesterday += total

    return total_revenue_today, total_revenue_yesterday


async def get_orders_count_by_month(restaurant_id: str) -> Tuple[Optional[int], Optional[int]]:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if not restaurant_ref:
        return None, None

    restaurant_data = restaurant_ref.get().to_dict()
    total_order_count_current_month = 0
    total_order_count_last_month = 0
    if "orders" in restaurant_data:
        # Assume orders_refs are fetched correctly as a list of DocumentReferences
        orders_refs: List[DocumentReference] = restaurant_data["orders"]

        # Filter orders for the current month
        current_month_orders = utils.get_documents_created_this_month(orders_refs)
        total_order_count_current_month = len(current_month_orders)

        # Filter orders for the previous month
        last_month_orders = utils.get_documents_created_last_month(orders_refs)
        total_order_count_last_month = len(last_month_orders)


    return total_order_count_current_month, total_order_count_last_month


async def get_orders_count_by_day(restaurant_id: str) -> Tuple[Optional[int], Optional[int]]:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if not restaurant_ref:
        return None, None

    restaurant_data = restaurant_ref.get().to_dict()
    total_order_count_today = 0
    total_order_count_yesterday = 0
    if "orders" in restaurant_data:
        # Assume orders_refs are fetched correctly as a list of DocumentReferences
        orders_refs: List[DocumentReference] = restaurant_data["orders"]

        # Filter orders for the current month
        current_month_orders = utils.get_documents_created_today(orders_refs)
        total_order_count_today = len(current_month_orders)

        # Filter orders for the previous month
        last_month_orders = utils.get_documents_created_yesterday(orders_refs)
        total_order_count_yesterday = len(last_month_orders)


    return total_order_count_today, total_order_count_yesterday


async def get_order_total(order_id: str) -> float or None:
    order_ref = await order_crud.get_order(order_id)
    if order_ref:
        order_data = order_ref.get().to_dict()

        return order_data["total"]
    return None


