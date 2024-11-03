from fastapi import FastAPI, HTTPException, Depends,UploadFile
from models import Document
from sqlalchemy.orm import Session
from database import get_db
from services import store_document_metadata, answermethod


app=FastAPI()


cache = {}
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile, db: Session = Depends(get_db)):

    doc_id = store_document_metadata(db, file)
    return {"document_id": doc_id, "message": "PDF uploaded successfully"}


@app.post("/ask/{doc_id}")
async def ask_question(doc_id: int, question: str, db: Session = Depends(get_db)):
    # Fetch the document based on doc_id
    if 'doc_id' in cache:
       content=cache[doc_id]
    else :
     cache[doc_id]=db.query(Document).filter(Document.id == doc_id).first().content
     content=cache[doc_id]
    
    if not content:
        raise HTTPException(status_code=404, detail="Document not found")

    # Assuming `answermethod` takes the document and question as arguments
    answer = answermethod(content, question)
    
    return {"Question": question, "Answer": answer}

