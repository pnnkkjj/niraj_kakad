import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [hotels, setHotels] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [selectedHotel, setSelectedHotel] = useState('');
  const [checkInDate, setCheckInDate] = useState('');
  const [checkOutDate, setCheckOutDate] = useState('');

  useEffect(() => {
    // Fetch hotels data from backend API
    axios.get('/hotels/')
      .then(response => {
        setHotels(response.data);
      })
      .catch(error => {
        console.error('Error fetching hotels:', error);
      });

    // Fetch bookings data for the logged-in user from backend API
    // Assuming the user ID is hard-coded for simplicity
    const userId = 1;
    axios.get(`/bookings/${userId}`)
      .then(response => {
        setBookings(response.data);
      })
      .catch(error => {
        console.error('Error fetching bookings:', error);
      });
  }, []);

  const handleBookRoom = () => {
    // Make a POST request to book a room
    const bookingData = {
      user_id: 1, // Assuming user ID is hard-coded
      room_id: selectedHotel.id, // Assuming room ID is based on selected hotel
      check_in_date: checkInDate,
      check_out_date: checkOutDate
    };

    axios.post('/bookings/', bookingData)
      .then(response => {
        console.log(response.data);
        // Refresh bookings data after successful booking
        axios.get(`/bookings/${1}`)
          .then(response => {
            setBookings(response.data);
          })
          .catch(error => {
            console.error('Error fetching bookings:', error);
          });
      })
      .catch(error => {
        console.error('Error booking room:', error);
      });
  };

  return (
    <div>
      <h1>Hotel Booking App</h1>
      <h2>Hotels</h2>
      <ul>
        {hotels.map(hotel => (
          <li key={hotel.id}>{hotel.name} - {hotel.location}</li>
        ))}
      </ul>

      <h2>Bookings</h2>
      <ul>
        {bookings.map(booking => (
          <li key={booking.id}>
            Room: {booking.room_id} - Check-in: {booking.check_in_date} - Check-out: {booking.check_out_date}
          </li>
        ))}
      </ul>

      <h2>Book a Room</h2>
      <select onChange={e => setSelectedHotel(hotels.find(hotel => hotel.id === parseInt(e.target.value)))}>
        <option value="">Select a hotel</option>
        {hotels.map(hotel => (
          <option key={hotel.id} value={hotel.id}>{hotel.name}</option>
        ))}
      </select>
      <br />
      Check-in Date: <input type="date" onChange={e => setCheckInDate(e.target.value)} /><br />
      Check-out Date: <input type="date" onChange={e => setCheckOutDate(e.target.value)} /><br />
      <button onClick={handleBookRoom}>Book Room</button>
    </div>
  );
}

export default App;