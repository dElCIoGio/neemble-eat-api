from google.cloud.firestore_v1.document import DocumentReference
from app.db import modifications_collection_ref, modification_options_collection_ref
from app.schemas import modification as modification_schema


async def create_modification(modification: modification_schema.ModificationCreate) -> DocumentReference:
	modification_data = {
		"name": modification.name,
		"description": modification.description,
		"price": modification.price,
		"imageURL": modification.imageURL,
		"restaurantID": modification.restaurantID,
	}
	ref = modifications_collection_ref.add(modification_data)
	return ref[1]


async def get_modification(modification_id: str) -> DocumentReference or None:
	modification = modifications_collection_ref.document(modification_id)
	doc = modification.get()
	return modification if doc.exists else None


async def update_modification(modification_id: str, update_data: dict) -> DocumentReference or None:
	modification = await get_modification(modification_id)
	if modification:
		modification.update(update_data)
	return modification


async def delete_modification(modification_id: str) -> DocumentReference or None:
	modification = await get_modification(modification_id)
	if modification:
		modification.delete()
	return modification


async def create_modification_option(modification_option: modification_schema.ModificationOptionCreate) -> DocumentReference:
	modification_option_data = {
		"name": modification_option.name,
		"description": modification_option.description,
		"price": modification_option.price,
		"imageURL": modification_option.imageURL,
		"modificationID": modification_option.modificationID,
	}
	ref = modification_options_collection_ref.add(modification_option_data)
	return ref[1]


async def get_modification_option(modification_option_id: str) -> DocumentReference or None:
	modification_option = modification_options_collection_ref.document(modification_option_id)
	doc = modification_option.get()
	return modification_option if doc.exists else None


async def update_modification_option(modification_option_id: str, update_data: dict) -> DocumentReference or None:
	modification_option = await get_modification_option(modification_option_id)
	if modification_option:
		modification_option.update(update_data)
	return modification_option


async def delete_modification_option(modification_option_id: str) -> DocumentReference or None:
	modification_option = await get_modification_option(modification_option_id)
	if modification_option:
		modification_option.delete()
	return modification_option