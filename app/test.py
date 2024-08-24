#from database.database import SessionLocal
#from database.models import *
#import decimal
#
#session = SessionLocal()
#
## Create and add a RestaurantRepresentant
#representant = Representant(firstName="John",
#                            lastName="Doe",
#                            role="Manager",
#                            phone_number="1234567890",
#                            UUID="thhjvburrtcyvubhjin7g")
#
#session.add(representant)
#session.commit()
#
## Create and add a Restaurant
#restaurant = Restaurant(name="Best Eats", address="123 Tasty St", phone_number="+440987654321",
#                        restaurantRepresentantId=representant.id)
#session.add(restaurant)
#session.commit()
#
## Create and add a Menu
#menu = Menu(restaurantId=restaurant.id, description="Main Menu", name="Dinner")
#session.add(menu)
#session.commit()
#
## Create and add a Category
#category = Category(name="Appetizers", description="Starters", menuId=menu.id)
#session.add(category)
#session.commit()
#
## Create and add a MenuItem
#menu_item = MenuItem(name="Spring Rolls", description="Crispy rolls", price=decimal.Decimal("5.99"),
#                     category_id=category.id, image_url="http://example.com/springrolls.jpg")
#session.add(menu_item)
#session.commit()
#
## Create and add a Table
#table = Table(link="http://example.com/table1", restaurantId=restaurant.id)
#session.add(table)
#session.commit()
#
## Create and add a Session
#tableSession = TableSession(startTime=datetime.now(), billed=False, tableId=table.id, restaurantId=restaurant.id)
#session.add(tableSession)
#session.commit()
#
## Create and add an Order
#order = Order(orderTime=datetime.now(), delivered=False, sessionId=tableSession.id)
#session.add(order)
#session.commit()
#
## Create and add an OrderItem
#order_item = OrderItem(quantity=2, menuItemId=menu_item.id, orderId=order.id)
#session.add(order_item)
#session.commit()
#
## Create and add an Invoice
#invoice = Invoice(total=decimal.Decimal("20.00"), generatedTime=datetime.now())
#session.add(invoice)
#session.commit()
#
## Associate Invoice with Session
#session.invoiceId = invoice.id
#session.commit()
#
## Query to verify
#print(session.query(Restaurant).all()[0].name)
#
#session.close()
#

from pydantic_extra_types.phone_numbers import PhoneNumber

number: str = "07927300098"
from phonenumbers import parse, geocoder, carrier, phonenumberutil

x = parse(number, "GB")
print(x)
print(geocoder.description_for_number(x, "en"))
#print(carrier.name_for_number(x, "en"))
