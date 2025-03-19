from fastapi import APIRouter, HTTPException, Response, File, UploadFile, Form, Request
from app.schemas import invitationToken as invitation_token_schema
from app.crud import invitationToken as invitation_token_crud


router = APIRouter()


@router.post("/{restaurant_id}/create-token", response_model=invitation_token_schema.InvitationTokenDisplay)
async def create_token(restaurant_id: str):
    invitation_token_ref = await invitation_token_crud.create_invitation_token(restaurant_id)
    if not invitation_token_ref:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return invitation_token_schema.InvitationToken.from_doc(invitation_token_ref)


@router.get("/{token_id}", response_model=invitation_token_schema.InvitationTokenDisplay)
async def get_token(token_id: str):
    invitation_token_ref = await invitation_token_crud.get_invitation_token(token_id)
    if not invitation_token_ref:
        raise HTTPException(status_code=404, detail="Token not found")
    return invitation_token_schema.InvitationToken.from_doc(invitation_token_ref)


@router.delete("/{token_id}", response_model=bool)
async def delete_token(token_id: str):
    invitation_token_ref = await invitation_token_crud.delete_invitation_token(token_id)
    if not invitation_token_ref:
        return False
    return True


@router.get("/{token_id}")
async def verify_token(token_id: str):
    invitation_token_ref = await invitation_token_crud.get_invitation_token(token_id)
    if not invitation_token_ref:
        return False
    return invitation_token_schema.InvitationToken.from_doc(invitation_token_ref)


