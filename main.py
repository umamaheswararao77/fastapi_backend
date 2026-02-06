from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from models import Inquiry
from schemas import InquiryCreate, InquiryResponse

# CREATE TABLES (AFTER MODELS IMPORT)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE INQUIRY
@app.put("/inquiries/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry(
    inquiry_id: int,
    data: InquiryCreate,
    db: Session = Depends(get_db)
):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()

    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    inquiry.name = data.name
    inquiry.email = data.email
    inquiry.phone = data.phone
    inquiry.message = data.message

    db.commit()
    db.refresh(inquiry)
    return inquiry

# READ INQUIRIES
@app.get("/inquiries", response_model=list[InquiryResponse])
def get_inquiries(db: Session = Depends(get_db)):
    return db.query(Inquiry).all()


@app.delete("/inquiries/{inquiry_id}")
def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()

    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    db.delete(inquiry)
    db.commit()

    return {"message": "Inquiry deleted successfully"}