from app.schemas.representant import RepresentantCreate
from google.cloud.firestore_v1.document import DocumentReference
from app import database


collection_ref = database.db.collection('representants')


def getRepresentant(representant_id: str) -> DocumentReference or None:
    represnetant = collection_ref.document(representant_id)
    doc = represnetant.get()
    return represnetant if doc.exists else None


def getRepresentantByUUID(UUID: str) -> DocumentReference or None:
    query = collection_ref.where('UUID', '==', UUID).limit(1).stream()
    for doc in query:
        return doc.reference
    return None


def createRepresentant(representant: RepresentantCreate) -> DocumentReference:
    representant_data = {
        "UUID": representant.UUID,
        "firstName": representant.firstName,
        "lastName": representant.lastName,
        "email": representant.email,
        "role": representant.role,
        "phoneNumber": representant.phoneNumber
    }
    ref = collection_ref.add(representant_data)
    return ref[1]


def updateRepresentant(representant_id: str, update_data: dict) -> DocumentReference or None:
    representant = getRepresentant(representant_id)
    if representant:
        representant.update(update_data)
    return representant


def deleteRepresentant(representant_id: str):
    representant = getRepresentant(representant_id)
    if representant:
        representant.delete()
    return representant

