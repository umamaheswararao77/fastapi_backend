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
    allow_origins=["http://localhost:5173"],
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
@app.post("/inquiries", response_model=InquiryResponse)
def create_inquiry(data: InquiryCreate, db: Session = Depends(get_db)):
    inquiry = Inquiry(**data.dict())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry

# READ INQUIRIES
@app.get("/inquiries", response_model=list[InquiryResponse])
def get_inquiries(db: Session = Depends(get_db)):
    return db.query(Inquiry).all()
