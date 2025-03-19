from app.schemas.invoice import InvoiceCreate
from app.crud.tableSession import get_table_session
from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime
from app.db import invoices_collection_ref



async def create_invoice(invoice: InvoiceCreate) -> DocumentReference or None:
    invoice_data = {
        "generatedTime": datetime.now(),
    }
    session_ref = await get_table_session(invoice.sessionID)
    if session_ref:
        session_data = session_ref.get().to_dict()
        orders: list[DocumentReference] = session_data["orders"] if "orders" in session_data else None
        if orders:
            total = 0
            for order_ref in orders:
                order_ref.update({"sessionStatus": "Billed"})
                order_data = order_ref.get().to_dict()
                order_total = float(order_data["total"])
                total += order_total
            invoice_data["sessionID"] = session_ref
            invoice_data["orders"] = orders
            invoice_data["total"] = total
            ref = invoices_collection_ref.add(invoice_data)
            return ref[1]


async def get_invoice(invoice_id: str):
    invoice = invoices_collection_ref.document(invoice_id)
    doc = invoice.get()
    return invoice if doc.exists else None


async def update_invoice(invoice_id: str, update_data: dict):
    invoice = await get_invoice(invoice_id)
    if invoice:
        invoice.update(update_data)
    return invoice


async def delete_invoice(invoice_id: str):
    invoice = await get_invoice(invoice_id)
    if invoice:
        invoice.delete()
    return invoice
