from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Hotel, Room, Booking
from typing import Optional


app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define API endpoints using the database models
@app.get("/hotels/")
def get_hotels(location: Optional[str] = None, db: Session = Depends(get_db)):
    if location:
        return db.query(Hotel).filter(Hotel.location == location).all()
    return db.query(Hotel).all()

@app.post("/bookings/")
def book_room(booking: Booking, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    if not room or not room.available:
        raise HTTPException(status_code=400, detail="Room not available")
    room.available = False
    db.add(booking)
    db.commit()
    return {"message": "Room booked successfully"}

@app.get("/bookings/{user_id}")
def get_bookings(user_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

@app.put("/bookings/{user_id}")
def modify_booking(user_id: int, booking: Booking, db: Session = Depends(get_db)):
    existing_booking = db.query(Booking).filter(Booking.user_id == user_id).first()
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    existing_booking.check_in_date = booking.check_in_date
    existing_booking.check_out_date = booking.check_out_date
    db.commit()
    return {"message": "Booking modified successfully"}

@app.delete("/bookings/{user_id}")
def cancel_booking(user_id: int, db: Session = Depends(get_db)):
    existing_booking = db.query(Booking).filter(Booking.user_id == user_id).first()
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    room = db.query(Room).filter(Room.id == existing_booking.room_id).first()
    room.available = True
    db.delete(existing_booking)
    db.commit()
    return {"message": "Booking canceled successfully"}