from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import invoice as invoice_crud
from app.schemas import invoice as invoice_schema
from app.utils import invoice as invoice_utils
from google.cloud.firestore_v1.document import DocumentReference


router = APIRouter()


@router.post("/", response_model=invoice_schema.InvoiceDisplay)
def create_invoice(invoice: invoice_schema.InvoiceCreate):
    invoice_ref: DocumentReference = invoice_crud.createInvoice(invoice=invoice)
    invoice_data = invoice_utils.json(invoice_ref)
    return invoice_schema.InvoiceDisplay(**invoice_data)


@router.get("/{invoice_id}", response_model=invoice_schema.InvoiceDisplay)
def read_invoice(invoice_id: str):
    invoice_ref = invoice_crud.getInvoice(invoice_id=invoice_id)
    if invoice_ref is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice_data = invoice_utils.json(invoice_ref)
    return invoice_schema.InvoiceDisplay(**invoice_data)


@router.put("/{invoice_id}", response_model=invoice_schema.InvoiceDisplay)
def update_invoice(invoice_id: str, invoice: invoice_schema.InvoiceBase):
    invoice_ref = invoice_crud.updateInvoice(invoice_id, invoice.dict(exclude_unset=True))
    if invoice_ref is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice_data = invoice_utils.json(invoice_ref)
    return invoice_schema.InvoiceDisplay(**invoice_data)


@router.delete("/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: str):
    invoice_ref = invoice_crud.deleteInvoice(invoice_id)
    if invoice_ref is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return Response(status_code=204)
