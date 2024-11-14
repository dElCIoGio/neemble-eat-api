from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from fastapi import FastAPI, File, Form, UploadFile


class Item(BaseModel):
    categoryID: str
    name: str
    description: str
    price: str
    availability: str


class ItemList(BaseModel):
    items: List[Item]

