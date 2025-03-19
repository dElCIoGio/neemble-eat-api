from app.schemas import user as user_schema
from google.cloud.firestore_v1.document import DocumentReference
from app.db import users_collection_ref


async def get_user(user_id: str) -> DocumentReference or None:
    user_ref = users_collection_ref.document(user_id)
    doc = user_ref.get()
    return user_ref if doc.exists else None


async def get_user_by_uuid(uuid: str) -> DocumentReference or None:
    query = users_collection_ref.where('UUID', '==', uuid).limit(1).stream()
    for doc in query:
        return doc.reference
    return None


async def create_user(user: user_schema.UserCreate) -> DocumentReference:
    user_data = {
        "UUID": user.UUID,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "role": user.role.model_dump(),
        "phoneNumber": user.phoneNumber
    }
    print(user_data)
    ref = users_collection_ref.add(user_data)
    return ref[1]


async def update_user(user_id: str, update_data: dict) -> DocumentReference or None:
    user = await get_user(user_id)
    if user:
        user.update(update_data)
    return user


async def delete_user(user_id: str):
    user = await get_user(user_id)
    if user:
        user.delete()
    return user
