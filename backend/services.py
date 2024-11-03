import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models import Document
from transformers import pipeline
from sqlalchemy.orm import Session



# Load the question-answering pipeline
qa_pipeline = pipeline("question-answering")

# Ensure the upload directory exists
if not os.path.exists('store'):
    print("going to create    ====")
    os.makedirs('store')

def store_document_metadata(db: Session, file: UploadFile) -> int:
    # Save the file locally
    file_path = os.path.join('store', file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Reset file pointer to beginning if further reads are needed
    file.file.seek(0)

    # Collect metadata from the uploaded PDF
    filename = file.filename
    upload_date = datetime.now()
    content = extract_text_from_pdf(file_path)  # Pass file path for extraction

    # Save metadata in DB (ensure Document model is imported)
    new_document = Document(filename=filename, upload_date=upload_date, content=content)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document.id

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF."""
    import fitz  # PyMuPDF
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def answermethod(content:str, question:str):
    print("We are inside answer method")
    try:
        print("We are inside answer method 1")
        result = qa_pipeline(question=question, context=content)
        print("We are inside answer method 2")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))