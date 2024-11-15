from google.cloud.firestore_v1.document import DocumentReference
from app import database
from app.schemas import modifier as modifier_schema


modifier_collection_ref = database.db.collection("modifiers")
modifier_option_collection_ref = database.db.collection("modifier options")


async def createModifier(modifier: modifier_schema.ModifierCreate) -> DocumentReference:
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
	modifier_ref = modifier_collection_ref.add(modifier_data)
	return modifier_ref[1]


async def getModifier(modifier_id: str) -> DocumentReference or None:
	modifier = modifier_collection_ref.document(modifier_id)
	doc = modifier.get()
	return modifier if doc.exists else None


async def updateModifier(modifier_id: str, update_data: dict) -> DocumentReference or None:
	modifier = await getModifier(modifier_id)
	if modifier:
		modifier.update(update_data)
	return modifier


async def deleteModifier(modifier_id: str) -> DocumentReference or None:
	modifier = await getModifier(modifier_id)
	if modifier:
		modifier.delete()
	return modifier


async def createModifierOption(modifier_option: modifier_schema.ModifierOptionCreate):
	modifier_option_data = {
		"name": modifier_option.name,
		"additionalPrice": modifier_option.additionalPrice,
	}
	modifier_option_ref = modifier_option_collection_ref.add(modifier_option_data)
	return modifier_option_ref[1]


async def getModifierOption(modifier_option_id: str) -> DocumentReference or None:
	modifier_option = modifier_option_collection_ref.document(modifier_option_id)
	doc = modifier_option.get()
	return modifier_option if doc.exists else None


async def updateModifierOption(modifier_option_id: str, update_data: dict) -> DocumentReference or None:
	modifier_option = await getModifierOption(modifier_option_id)
	if modifier_option:
		modifier_option.update(update_data)
	return modifier_option


async def deleteModifierOption(modifier_option_id: str) -> DocumentReference or None:
	modifier_option = await getModifierOption(modifier_option_id)
	if modifier_option:
		modifier_option.delete()
	return modifier_option
