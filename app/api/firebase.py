from fastapi import HTTPException, APIRouter
from app.firebase import auth
import firebase_admin

router = APIRouter()


@router.delete("/delete-user/{uid}")
async def delete_user(uid: str):
    try:
        auth.delete_user(uid)
        return {"message": f"Successfully deleted user with UID: {uid}"}
    except firebase_admin.exceptions.FirebaseError as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")