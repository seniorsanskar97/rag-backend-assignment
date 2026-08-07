from pydantic import BaseModel, EmailStr


class BookingRequest(BaseModel):
    name: str
    email: EmailStr
    date: str
    time: str


class BookingResponse(BaseModel):
    message: str