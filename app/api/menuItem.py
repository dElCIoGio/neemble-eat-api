from fastapi import APIRouter, HTTPException, Response, File, UploadFile, Form
from app.crud import menuItem as menu_item_crud
from app.schemas import menuItem as menu_item_schema
from app.utils import menuItem as menu_item_utils
from app.services import menuItem as menu_item_service

from pathlib import Path
import os
import aiofiles

router = APIRouter()
base_path = Path(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIRECTORY = base_path.parent / "uploads"
# UPLOAD_DIRECTORY.parent.mkdir(parents=True, exist_ok=True)


@router.post("/", summary="Creates a Menu Item", response_model=menu_item_schema.MenuItemDisplay)
async def create_menu_item(menu_item: menu_item_schema.MenuItemCreate):
    menu_item_ref = await menu_item_crud.createMenuItem(menu_item=menu_item)
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not created")
    menu_item_data = menu_item_utils.json(menu_item_ref)
    return menu_item_schema.MenuItemDisplay(**menu_item_data)


@router.get("/{menu_item_id}", summary="Retrieve an item by its ID from the database.",
            response_model=menu_item_schema.MenuItemDisplay)
async def read_menu_item(menu_item_id: str):
    """
    Retrieve an item by its ID from the database.

    Args:
        menu_item_id (str): The unique identifier for the item.

    Returns:
        Item: The retrieved item object.

    Raises:
        HTTPException: 404 error if the item is not found in the database.

    Examples:
        curl -X GET "http://localhost:8000/items/123" -H  "accept: application/json"
    """
    menu_item_ref = await menu_item_crud.getMenuItem(menu_item_id=menu_item_id)
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    menu_item_data = menu_item_utils.json(menu_item_ref)
    return menu_item_schema.MenuItemDisplay(**menu_item_data)


@router.put("/{menu_item_id}", response_model=menu_item_schema.MenuItemDisplay)
async def update_menu_item(
        menu_item_id: str,
        restaurant_id: str = Form(...),
        name: str = Form(None),
        imageFile: UploadFile = File(None),
        price: str = Form(None),
        categoryID: str = Form(None),
        availability: str = Form(None),
        description: str = Form(None)):
    print(name)
    print(price)
    print(categoryID)
    print(availability)
    print(description)
    if imageFile:
        safe_filename = imageFile.filename.replace("/", "_").replace("\\", "_").replace("..", "_")
        file_location = UPLOAD_DIRECTORY / safe_filename
        try:
            async with aiofiles.open(file_location, "wb") as buffer:
                await buffer.write(await imageFile.read())
        except Exception as error:
            print("Error:", error)
            file_location = None
    else:
        file_location = None

    menu_item_ref = await menu_item_service.update_menu_item(
        menu_item_id=menu_item_id,
        restaurant_id=restaurant_id,
        name=name,
        description=description,
        file_path=file_location,
        categoryID=categoryID,
        availability=True if availability == "True" else False,
        price=float(price) if price is not None else None
    )
    if file_location:
        os.remove(file_location)
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    menu_item_data = menu_item_utils.json(menu_item_ref)
    return menu_item_schema.MenuItemDisplay(**menu_item_data)


@router.delete("/{menu_item_id}", status_code=204)
async def delete_menu_item(menu_item_id: str):
    menu_item_ref = await menu_item_crud.deleteMenuItem(menu_item_id)
    if menu_item_ref is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return Response(status_code=204)
