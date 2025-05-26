# 🎟️ Event Ticketing System - FastAPI

A simple in-memory Event Ticketing backend built using **FastAPI**. This API supports:

- Event creation, listing, update, and deletion
- User registration with email and role
- Ticket booking (one per user per event)
- Pagination and validation

---

## 🚀 Features

- ✅ CRUD operations for **Events**
- ✅ Ticket purchase with **capacity** checks
- ✅ Unique ticket per user per event
- ✅ User creation with email and role
- ✅ Pagination support on event listing
- ✅ In-memory data persistence
- ✅ Input validation with Pydantic

---

## 📦 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) - Python Web Framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation and parsing
- [Uvicorn](https://www.uvicorn.org/) - ASGI server for FastAPI

---

## 🏗️ Project Structure

```
.
├── main.py             # Main FastAPI app
├── README.md           # You're reading it :)
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/event-ticketing-fastapi.git
   cd event-ticketing-fastapi
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Open API Docs**
   - Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔌 API Endpoints

### 📅 Events

- `POST /events` → Create event
- `GET /events?offset=0&limit=10` → List events
- `GET /events/{event_id}` → Get event details
- `PUT /events/{event_id}` → Update event
- `DELETE /events/{event_id}` → Delete event

### 👤 Users

- `POST /users` → Create a new user (email & role)

### 🎫 Tickets

- `POST /events/{event_id}/tickets` → Purchase a ticket (requires name and email)
- `GET /users/{user_id}/tickets` → Get all tickets purchased by a user

---

## 📝 Example Payloads

### Create Event
```json
POST /events
{
  "name": "IPL Final",
  "description": "Chennai vs Bangalore",
  "date": "2025-06-01",
  "capacity": 100,
  "venue": "Mumbai"
}
```

### Create User
```json
POST /users
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "attendee"
}
```

### Purchase Ticket
```http
POST /events/{event_id}/tickets?email=john@example.com&name=John Doe
```

---

## ✅ To Do (Enhancements)

- [ ] Add persistent storage (e.g., SQLite or PostgreSQL)
- [ ] Add JWT-based authentication
- [ ] Implement advanced search/filtering for events
- [ ] Add role-based access for admins

---

## 🧑‍💻 Author

**Your Name** – [your.email@example.com](mailto:your.email@example.com)  
Feel free to reach out for collaboration or questions!

---

## 📜 License

This project is licensed under the MIT License.