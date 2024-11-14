from fastapi import APIRouter, HTTPException, Response, File, UploadFile, Form, Request

from app.crud import category as category_crud
from app.schemas import category as category_schema
from app.schemas import menuItem as menu_item_schema
from app.services import category as category_service
from app.utils import category as category_utils
from app.utils import menuItem as menu_item_utils
from app.schemas import newItem as new_item_schema

import os
import aiofiles
from pathlib import Path
from typing import List
import json


router = APIRouter()
base_path = Path(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIRECTORY = base_path.parent / "uploads"
# UPLOAD_DIRECTORY.parent.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=category_schema.CategoryDisplay)
async def create_category(category: category_schema.CategoryCreate):
    category_ref = await category_crud.createCategory(category=category)
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not created")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.get("/{category_id}", response_model=category_schema.CategoryDisplay)
async def read_category(category_id: str):
    category_ref = await category_crud.getCategory(category_id=category_id)
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.put("/{category_id}", response_model=category_schema.CategoryDisplay)
async def update_category(category_id: str, category: category_schema.CategoryBase):
    category_ref = await category_crud.updateCategory(category_id, category.model_dump(exclude_unset=True))
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str):
    category_ref = await category_service.delete_category_and_items(category_id)
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return Response(status_code=204)


# Services


@router.post("/menu-item/", response_model=menu_item_schema.MenuItemDisplay)
async def add_category_item(
        name: str = Form(...),
        description: str = Form(...),
        price: str = Form(...),
        imageFile: UploadFile = File(...),
        categoryID: str = Form(...),
        availability: str = Form(...)
):
    safe_filename = imageFile.filename.replace("/", "_").replace("\\", "_").replace("..", "_")
    file_location = UPLOAD_DIRECTORY / safe_filename

    try:
        async with aiofiles.open(file_location, "wb") as buffer:
            await buffer.write(await imageFile.read())

        menu_item = menu_item_schema.MenuItemCreate(
            name=name,
            description=description,
            categoryID=categoryID,
            availability=True if availability == "True" else False,
            price=float(price),
            imageURL=f"{file_location}"
        )

        item_ref = await category_service.add_item(categoryID, menu_item)
        if not item_ref:
            raise HTTPException(status_code=404, detail="The menu does not exist.")
        item_data = menu_item_utils.json(item_ref)
        if file_location.exists():
            os.remove(file_location)
        return menu_item_schema.MenuItemDisplay(**item_data)

    except Exception as error:
        print("Error: ", error)


async def add_category_items(items_categoryID: List[str] = Form(...),
                             items_name: List[str] = Form(...),
                             items_description: List[str] = Form(...),
                             items_price: List[str] = Form(...),
                             items_imageFile: List[UploadFile] = File(...),
                             items_availability: List[str] = File(...)
                             ):
    items = [
        {
            "category_id": category_id,
            "name": name,
            "description": description,
            "price": float(price),
            "image_file": image_file,
            "availability": bool(availability)
        }
        for category_id, name, description, price, image_file, availability
        in zip(items_categoryID, items_name, items_description, items_price, items_imageFile, items_availability)
    ]
    new_items: List[menu_item_schema.MenuItemDisplay] = []
    for item in items:
        print(item)
        image_file = item["image_file"]
        file_location = UPLOAD_DIRECTORY / image_file.filename
        with open(file_location, "wb") as buffer:
            buffer.write(await image_file.read())

        menu_item = menu_item_schema.MenuItemCreate(
            name=item["name"],
            description=item["description"],
            categoryID=item["category_id"],
            availability=item["availability"],
            price=item["price"],
            imageURL=str(file_location),
        )

        item_ref = await category_service.add_item(item["category_id"], menu_item)
        if not item_ref:
            raise HTTPException(status_code=404, detail="The menu does not exist.")
        item_data = menu_item_utils.json(item_ref)
        new_items.append(menu_item_schema.MenuItemDisplay(**item_data))
    return new_items


@router.post("/add-menu-items")
async def create_items(items: List[new_item_schema.Item], imageFiles: List[UploadFile] = File(...)):
    print(items)
    try:
        for item, imageFile in zip(items, imageFiles):
            print(item)
            contents = await imageFile.read()  # Read file content
            # Process file here, e.g., save to disk
        # Further process items
        return {"status": "items received", "number_of_items": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{category_id}/{menu_item_id}/menuItem", response_model=category_schema.CategoryDisplay)
async def remove_category_item(category_id: str, menu_item_id: str):
    category_ref = await category_service.remove_item(category_id, menu_item_id)
    if not category_ref:
        raise HTTPException(status_code=404, detail="Either the menu or the category does not exist.")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)


@router.delete("/{category_id}/menu-items", response_model=category_schema.CategoryDisplay)
async def remove_category_items(category_id: str, menu_item_ids: List[str]):
    category_ref = await category_service.remove_items(category_id, menu_item_ids)
    if category_ref is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    category_data = category_utils.json(category_ref)
    return category_schema.CategoryDisplay(**category_data)
