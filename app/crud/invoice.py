from app.schemas.invoice import InvoiceCreate
from app.crud.tableSession import getTableSession
from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime
from app import database


collection_ref = database.db.collection('invoices')


def createInvoice(invoice: InvoiceCreate) -> DocumentReference or None:
    invoice_data = {
        "generatedTime": datetime.now(),
    }
    session_ref = getTableSession(invoice.sessionID)
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
            ref = collection_ref.add(invoice_data)
            return ref[1]


def getInvoice(invoice_id: str):
    invoice = collection_ref.document(invoice_id)
    doc = invoice.get()
    return invoice if doc.exists else None


def updateInvoice(invoice_id: str, update_data: dict):
    invoice = getInvoice(invoice_id)
    if invoice:
        invoice.update(update_data)
    return invoice


def deleteInvoice(invoice_id: str):
    invoice = getInvoice(invoice_id)
    if invoice:
        invoice.delete()
    return invoice
