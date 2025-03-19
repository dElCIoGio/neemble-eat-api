from app.utils import utils
from google.cloud.firestore_v1.document import DocumentReference
from app.crud import restaurant as restaurant_crud
from app.db import invitation_tokens_collection_ref


async def create_invitation_token(restaurant_id: str) -> DocumentReference:
    restaurant_ref = await restaurant_crud.get_restaurant(restaurant_id)
    if restaurant_ref:
        expire_time = utils.get_time_plus_hs()
        invitation_token = {
            "restaurant_id": restaurant_ref,
            "expire": expire_time
        }
        ref = invitation_tokens_collection_ref.add(invitation_token)
        return ref[1]

async def get_invitation_token(token_id: str):
    token = invitation_tokens_collection_ref.document(token_id)
    doc = token.get()
    return token if doc.exists else None

async def update_invitation_token(token_id: str, update_data: dict):
    token = await get_invitation_token(token_id)
    if token:
        token.update(update_data)
    return token

async def delete_invitation_token(token_id: str):
    token = await get_invitation_token(token_id)
    if token:
        token.delete()
    return token