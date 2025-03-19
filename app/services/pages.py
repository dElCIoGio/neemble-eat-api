from google.cloud.firestore_v1.document import DocumentReference
from app.crud import table as table_crud
from app.services.menu import get_parsed_menu


async def get_menu_page(table_id: str):
    try:
        table_ref = await table_crud.get_table(table_id=table_id)
        if table_ref:
            table_data = table_ref.get().to_dict()
            restaurant_ref: DocumentReference = table_data["restaurantID"]
            restaurant_data = restaurant_ref.get().to_dict()
            menu_ref: DocumentReference = restaurant_data["menus"][0]
            menu_id = menu_ref.id
            menu = await get_parsed_menu(menu_id)
            if menu_ref.get().exists and restaurant_ref.get().exists:
                return menu, restaurant_ref
        return None
    except Exception as error:
        print(error)