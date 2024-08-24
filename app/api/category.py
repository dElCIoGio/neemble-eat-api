from fastapi import APIRouter, HTTPException, Response
from app.crud import category as category_crud
from app.schemas import category as category_schema
from app.schemas import menuItem as menu_item_schema
from app.services import category as category_service
from app.utils import category as category_utils
from app.utils import menuItem as menu_item_utils


router = APIRouter()


@router.post("/", response_model=category_schema.CategoryDisplay)
def create_category(category: category_schema.CategoryCreate):
    category_ref = category_crud.createCategory(category=category)
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.get("/{category_id}", response_model=category_schema.CategoryDisplay)
def read_category(category_id: str):
    category_ref = category_crud.getCategory(category_id=category_id)
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.put("/{category_id}", response_model=category_schema.CategoryDisplay)
def update_category(category_id: str, category: category_schema.CategoryBase):
    category_ref = category_crud.updateCategory(category_id, category.dict(exclude_unset=True))
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: str):
    category_ref = category_service.delete_category_and_items(category_id)
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return Response(status_code=204)


# Services


@router.post("/{category_id}/menuItem", response_model=menu_item_schema.MenuItemDisplay)
def add_category_item(category_id: str, menu_item: menu_item_schema.MenuItemCreate):
    item_ref = category_service.add_item(category_id, menu_item)
    if not item_ref:
        raise HTTPException(status_code=404, detail="The menu does not exist.")
    item_data = menu_item_utils.json(item_ref)
    return menu_item_schema.MenuItemDisplay(**item_data)


@router.delete("/{category_id}/{menu_item_id}/menuItem", response_model=category_schema.CategoryDisplay)
def remove_category_item(category_id: str, menu_item_id: str):
    category_ref = category_service.remove_item(category_id, menu_item_id)
    if not category_ref:
        raise HTTPException(status_code=404, detail="Either the menu or the category does not exist.")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)