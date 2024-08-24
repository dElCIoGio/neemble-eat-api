from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import representant as representant_crud
from app.schemas import representant as representant_schema
from app.utils import representant as representant_utils


router = APIRouter()


@router.post("/", response_model=representant_schema.RepresentantDisplay)
def create_representant(representant: representant_schema.RepresentantCreate):
    representant_ref = representant_crud.createRepresentant(representant=representant)
    if representant_ref is None:
        raise HTTPException(status_code=400, detail="There was an error creating the representant account")
    representant_data = representant_utils.json(representant_ref)
    return representant_schema.RepresentantDisplay(**representant_data)


@router.get("/{representant_id}", response_model=representant_schema.RepresentantDisplay)
def read_representant(representant_id: str):
    representant_ref = representant_crud.getRepresentant(representant_id=representant_id)
    if representant_ref is None:
        raise HTTPException(status_code=404, detail="Representant not found")
    representant_data = representant_utils.json(representant_ref)
    print(representant_data)
    return representant_schema.RepresentantDisplay(**representant_data)


@router.get("/{UUID}/UUID", response_model=representant_schema.RepresentantDisplay)
def read_representant(UUID: str):
    representant_ref = representant_crud.getRepresentantByUUID(UUID=UUID)
    if representant_ref is None:
        raise HTTPException(status_code=404, detail="Representant not found")
    representant_data = representant_utils.json(representant_ref)
    print(representant_data)
    return representant_schema.RepresentantDisplay(**representant_data)


@router.put("/{representant_id}", response_model=representant_schema.RepresentantDisplay)
def update_representant(representant_id: str, representant: representant_schema.RepresentantBase):
    representant_ref = representant_crud.updateRepresentant(representant_id, representant.dict(exclude_unset=True))
    if representant_ref is None:
        raise HTTPException(status_code=404, detail="Representant not found")
    representant_data = representant_utils.json(representant_ref)
    return representant_schema.RepresentantDisplay(**representant_data)


@router.delete("/{representant_id}", status_code=204)
def delete_representant(representant_id: str):
    representant_ref = representant_crud.deleteRepresentant(representant_id)
    if representant_ref is None:
        raise HTTPException(status_code=404, detail="Representant not found")
    return Response(status_code=204)
