from app.crud import restaurant as restaurant_crud
from app.crud import menu as menu_crud
from app.schemas import restaurant as restaurant_schems
from app.schemas import category as category_schema
from app.schemas import menu as menu_schemas

from app.services import restaurant as restaurant_service
from app.services import menu as menu_service
from typing import List

# ALL OF THIS IS USELESS


async def conclude_account_setup(
        representantID: str,
        categories: List[category_schema.CategoryCreate],
        number_of_tables: int,
        name: str,
        address: str,
        phone_number: str,
        bannerFile: str,
        description: str):
    restaurant_ref = await create_restaurant(name,
                                             address,
                                             phone_number,
                                             bannerFile,
                                             description)
    if restaurant_ref:
        try:
            await restaurant_service.assign_manager(restaurant_ref.id, representantID)
        except Exception as error:
            print(error)
        else:
            menu_ref = await create_menu("Menu", restaurant_ref.id)
            if menu_ref:
                for category in categories:
                    await menu_service.add_category(menu_ref.id, category)

        for number in range(0, number_of_tables):
            table_ref = restaurant_service.add_table(restaurant_ref.id)


async def create_restaurant(name: str,
                            address: str,
                            phone_number: str,
                            bannerFile: str,
                            description: str):
    restaurant = restaurant_schems.RestaurantCreate(
        name=name,
        address=address,
        phoneNumber=phone_number,
        bannerURL=bannerFile,
        description=description,
        orders=None,
        representants=None,
        sessions=None,
        menus=None,
        tables=None
    )
    restaurant_ref = await restaurant_crud.createRestaurant(restaurant)
    return restaurant_ref


async def create_menu(name: str, restaurant_id: str):
    menu = menu_schemas.MenuCreate(
        restaurantID=restaurant_id,
        name=name,
        description=None,
        categories=None
    )
    menu_ref = menu_crud.createMenu(menu)
    return menu_ref
