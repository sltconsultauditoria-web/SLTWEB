
from fastapi import APIRouter, UploadFile, File
from pymongo import MongoClient
from datetime import datetime
import os

router = APIRouter(prefix="/api/ocr", tags=["OCR"])

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    nome = file.filename

    data = {
        "arquivo": nome,
        "texto_extraido": "OCR pronto para integrar pytesseract",
        "data": datetime.utcnow()
    }

    db.ocr_documentos.insert_one(data)

    return {"ok": True, "arquivo": nome}

@router.get("/lista")
def lista():
    docs = list(db.ocr_documentos.find({}, {"_id":0}))
    return docs
