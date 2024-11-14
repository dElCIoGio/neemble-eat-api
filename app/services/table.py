from google.cloud.firestore_v1 import DocumentReference
from app.services import restaurant as restaurant_service
from app.crud import table as table_crud
from typing import Optional


async def get_table_session(table_id: str) -> Optional[DocumentReference]:

	async def get_table_data(table_id: str) -> Optional[dict]:
		table_ref = await table_crud.getTable(table_id)
		if table_ref:
			return table_ref.get().to_dict()
		return None

	def get_current_session_ref(table_data: dict) -> Optional[DocumentReference]:
		return table_data.get("currentSessionID")

	def get_restaurant_ref(table_data: dict) -> DocumentReference:
		return table_data["restaurantID"]

	table_data = await get_table_data(table_id)
	if table_data is None:
		return None

	current_session_ref = get_current_session_ref(table_data)
	if current_session_ref and current_session_ref.get().exists:
		return current_session_ref

	restaurant_ref = get_restaurant_ref(table_data)
	new_session_ref = await restaurant_service.add_session(
		table_id=table_id,
		restaurant_id=restaurant_ref.id
	)

	return new_session_ref
