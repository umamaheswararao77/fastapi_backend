from pydantic import BaseModel

class InquiryCreate(BaseModel):
    name: str
    email: str
    phone: str
    message: str

class InquiryResponse(InquiryCreate):
    id: int

    class Config:
        from_attributes = True
