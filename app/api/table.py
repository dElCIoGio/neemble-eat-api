from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import table as table_crud
from app.schemas import table as table_schema
from app.utils import table as table_utils


router = APIRouter()


@router.post("/", response_model=table_schema.TableDisplay)
def create_table(table: table_schema.TableCreate):
    table_ref = table_crud.createTable(table=table)
    if table_ref is None:
        raise HTTPException(status_code=400, detail="There was an error creating the table.")
    table_data = table_utils.json(table_ref)
    return table_schema.TableDisplay(**table_data)


@router.get("/{table_id}", response_model=table_schema.TableDisplay)
def read_table(table_id: str):
    table_ref = table_crud.getTable(table_id=table_id)
    if table_ref is None:
        raise HTTPException(status_code=404, detail="Table not found")
    table_data = table_utils.json(table_ref)
    return table_schema.TableDisplay(**table_data)


@router.put("/{table_id}", response_model=table_schema.TableDisplay)
def update_table(table_id: str, table: table_schema.TableBase):
    table_ref = table_crud.updateTable(table_id, table.dict(exclude_unset=True))
    if table_ref is None:
        raise HTTPException(status_code=404, detail="Table not found")
    table_data = table_utils.json(table_ref)
    return table_schema.TableDisplay(**table_data)


@router.delete("/{table_id}", status_code=204)
def delete_table(table_id: str):
    table_ref = table_crud.deleteTable(table_id)
    if table_ref is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return Response(status_code=204)
