from google.cloud.firestore_v1.document import DocumentReference
from app.db import modifiers_collection_ref, modifier_options_collection_ref
from app.schemas import modifier as modifier_schema




async def create_modifier(modifier: modifier_schema.ModifierCreate) -> DocumentReference:
	modifier_data = {
		"name": modifier.name,
		"isRequired": modifier.isRequired,
		"limitType": modifier.limitType,
		"limit": modifier.limit,
		"optionLimitType": modifier.optionLimitType,
		"optionLimit": modifier.optionLimit,
		"description": modifier.description,
		"options": modifier.options,
	}
	modifier_ref = modifiers_collection_ref.add(modifier_data)
	return modifier_ref[1]


async def get_modifier(modifier_id: str) -> DocumentReference or None:
	modifier = modifiers_collection_ref.document(modifier_id)
	doc = modifier.get()
	return modifier if doc.exists else None


async def update_modifier(modifier_id: str, update_data: dict) -> DocumentReference or None:
	modifier = await get_modifier(modifier_id)
	if modifier:
		modifier.update(update_data)
	return modifier


async def delete_modifier(modifier_id: str) -> DocumentReference or None:
	modifier = await get_modifier(modifier_id)
	if modifier:
		modifier.delete()
	return modifier


async def create_modifier_option(modifier_option: modifier_schema.ModifierOptionCreate):
	modifier_option_data = {
		"name": modifier_option.name,
		"additionalPrice": modifier_option.additionalPrice,
	}
	modifier_option_ref = modifier_options_collection_ref.add(modifier_option_data)
	return modifier_option_ref[1]


async def get_modifier_option(modifier_option_id: str) -> DocumentReference or None:
	modifier_option = modifier_options_collection_ref.document(modifier_option_id)
	doc = modifier_option.get()
	return modifier_option if doc.exists else None


async def update_modifier_option(modifier_option_id: str, update_data: dict) -> DocumentReference or None:
	modifier_option = await get_modifier_option(modifier_option_id)
	if modifier_option:
		modifier_option.update(update_data)
	return modifier_option


async def delete_modifier_option(modifier_option_id: str) -> DocumentReference or None:
	modifier_option = await get_modifier_option(modifier_option_id)
	if modifier_option:
		modifier_option.delete()
	return modifier_option
