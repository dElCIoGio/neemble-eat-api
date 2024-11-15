from google.cloud.firestore_v1.document import DocumentReference
from app import database
from app.schemas import modification as modification_schema


modification_collection_ref = database.db.collection("modifications")
modification_option_collection_ref = database.db.collection("modification options")


async def createModification(modification: modification_schema.ModificationCreate) -> DocumentReference:
	modification_data = {
		"name": modification.name,
		"description": modification.description,
		"price": modification.price,
		"imageURL": modification.imageURL,
		"restaurantID": modification.restaurantID,
	}
	ref = modification_collection_ref.add(modification_data)
	return ref[1]


async def getModification(modification_id: str) -> DocumentReference or None:
	modification = modification_collection_ref.document(modification_id)
	doc = modification.get()
	return modification if doc.exists else None


async def updateModification(modification_id: str, update_data: dict) -> DocumentReference or None:
	modification = await getModification(modification_id)
	if modification:
		modification.update(update_data)
	return modification


async def deleteModification(modification_id: str) -> DocumentReference or None:
	modification = await getModification(modification_id)
	if modification:
		modification.delete()
	return modification


async def createModificationOption(modification_option: modification_schema.ModificationOptionCreate) -> DocumentReference:
	modification_option_data = {
		"name": modification_option.name,
		"description": modification_option.description,
		"price": modification_option.price,
		"imageURL": modification_option.imageURL,
		"modificationID": modification_option.modificationID,
	}
	ref = modification_option_collection_ref.add(modification_option_data)
	return ref[1]


async def getModificationOption(modification_option_id: str) -> DocumentReference or None:
	modification_option = modification_option_collection_ref.document(modification_option_id)
	doc = modification_option.get()
	return modification_option if doc.exists else None


async def updateModificationOption(modification_option_id: str, update_data: dict) -> DocumentReference or None:
	modification_option = await getModificationOption(modification_option_id)
	if modification_option:
		modification_option.update(update_data)
	return modification_option