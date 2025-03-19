from fastapi import APIRouter, HTTPException, Response
from app.crud import user as user_crud
from app.schemas import user as user_schema
from app.utils import user as user_utils
from fastapi_cache.decorator import cache
from app.api import CacheTime


router = APIRouter()


@router.post("/", response_model=user_schema.UserDisplay)
async def create_user(user: user_schema.UserCreate):
    user_ref = await user_crud.create_user(user=user)
    if user_ref is None:
        raise HTTPException(status_code=400, detail="There was an error creating the user account")
    user_data = user_utils.json(user_ref)
    return user_schema.UserDisplay(**user_data)


@router.get("/{user_id}", response_model=user_schema.UserDisplay)
async def read_user(user_id: str):
    user_ref = await user_crud.get_user(user_id=user_id)
    if user_ref is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_utils.json(user_ref)
    return user_schema.UserDisplay(**user_data)


@router.get("/{uuid}/UUID", response_model=user_schema.UserDisplay)
@cache(expire=CacheTime.GET_USER_BY_UUID)
async def get_user_by_uuid(uuid: str):
    user_ref = await user_crud.get_user_by_uuid(uuid=uuid)
    if user_ref is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_utils.json(user_ref)
    return user_schema.UserDisplay(**user_data)


@router.put("/{user_id}", response_model=user_schema.UserDisplay)
async def update_user(user_id: str, user: user_schema.UserBase):
    user_ref = await user_crud.update_user(user_id, user.model_dump(exclude_unset=True))
    if user_ref is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_utils.json(user_ref)
    return user_schema.UserDisplay(**user_data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    user_ref = await user_crud.delete_user(user_id)
    if user_ref is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
