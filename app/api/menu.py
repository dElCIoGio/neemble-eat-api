from fastapi import APIRouter, HTTPException, Response

from app.crud import menu as menu_crud
from app.schemas import menu as menu_schema
from app.schemas import category as category_schema
from app.services import menu as menu_services
from app.utils import menu as menu_utils
from app.utils import category as category_utils

router = APIRouter()


@router.post("/", response_model=menu_schema.MenuDisplay)
async def create_menu(menu: menu_schema.MenuCreate):
    menu_ref = await menu_crud.create_menu(menu=menu)
    if menu_ref is None:
        raise HTTPException(status_code=404, detail="Failed to create the menu")
    menu_data = menu_utils.json(menu_ref)
    return menu_schema.MenuDisplay(**menu_data)


@router.get("/{menu_id}", response_model=menu_schema.MenuDisplay)
async def read_menu(menu_id: str):
    menu_ref = await menu_crud.get_menu(menu_id=menu_id)
    if menu_ref is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu_data = menu_utils.json(menu_ref)
    return menu_schema.MenuDisplay(**menu_data)


@router.put("/{menu_id}", response_model=menu_schema.MenuDisplay)
async def update_menu(menu_id: str, menu: menu_schema.MenuBase):
    menu_ref = await menu_crud.update_menu(menu_id, menu.model_dump(exclude_unset=True))
    if menu_ref is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu_data = menu_utils.json(menu_ref)
    return menu_schema.MenuDisplay(**menu_data)


@router.delete("/{menu_id}", status_code=204)
async def delete_menu(menu_id: str):
    menu_ref = await menu_services.delete_menu_and_categories(menu_id)
    if menu_ref is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return Response(status_code=204)


# Services


@router.post("/{menu_id}/categories", response_model=category_schema.CategoryDisplay)
async def add_menu_category(menu_id: str, category: category_schema.CategoryCreate):
    category_ref = await menu_services.add_category(menu_id, category)
    if not category_ref:
        raise HTTPException(status_code=404, detail="Menu not found.")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.delete("/{menu_id}/{category_id}/categories", response_model=menu_schema.MenuDisplay)
async def remove_menu_category(menu_id: str, category_id: str):
    menu_ref = await menu_services.remove_category(menu_id, category_id)
    if not menu_ref:
        raise HTTPException(status_code=404, detail="Either the menu or the category does not exist.")
    menu_data = menu_utils.json(menu_ref)
    return menu_schema.MenuDisplay(**menu_data)


@router.get("/{menu_id}/parse")
async def get_parsed_menu(menu_id: str):
    categories = await menu_services.get_parsed_menu(menu_id)
    if not categories or len(categories) == 0:
        raise HTTPException(status_code=404, detail="Menu not found.")
    if len(categories) == 0:
        raise HTTPException(status_code=404, detail="Menu not found.")
    return categories

