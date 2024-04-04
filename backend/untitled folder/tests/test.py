from typing import Optional
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_hotels():
    response = client.get("/hotels/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_book_room():
    # Assuming we have valid booking data to test with
    booking_data = {
        "user_id": 1,
        "room_id": 1,
        "check_in_date": "2024-04-10",
        "check_out_date": "2024-04-15"
    }
    response = client.post("/bookings/", json=booking_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Room booked successfully"

def test_get_bookings():
    user_id = 1  # Assuming user with ID 1 has bookings
    response = client.get(f"/bookings/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_modify_booking():
    user_id = 1  # Assuming user with ID 1 has bookings
    booking_data = {
        "user_id": 1,
        "room_id": 1,
        "check_in_date": "2024-04-12",
        "check_out_date": "2024-04-18"
    }
    response = client.put(f"/bookings/{user_id}", json=booking_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Booking modified successfully"

def test_cancel_booking():
    user_id = 1  # Assuming user with ID 1 has bookings
    response = client.delete(f"/bookings/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Booking canceled successfully"