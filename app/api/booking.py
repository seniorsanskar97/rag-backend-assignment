from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingRequest, BookingResponse

router = APIRouter(
    prefix="/api/v1/booking",
    tags=["Interview Booking"],
)


@router.post("/", response_model=BookingResponse)
def book_interview(
    request: BookingRequest,
    db: Session = Depends(get_db),
):
    booking = Booking(
        name=request.name,
        email=request.email,
        date=request.date,
        time=request.time,
    )

    db.add(booking)
    db.commit()

    return BookingResponse(
        message="Interview booked successfully."
    )