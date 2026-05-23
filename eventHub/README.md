# EventHub - Event Management API

EventHub is a Django REST Framework-based API for managing events and reservations. It allows users to create, retrieve, update, and delete events, as well as manage event reservations with real-time seat availability tracking.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Models](#models)

## Features

- ✅ **Event Management**: Create, read, update, and delete events
- ✅ **Real-time Seat Tracking**: Automatic availability management
- ✅ **Reservations**: Book seats for events with validation
- ✅ **Cancellation**: Cancel reservations and restore seats
- ✅ **Filtering**: Filter events by status and venue
- ✅ **Data Validation**: Comprehensive validation for all operations

## Prerequisites

- Python 3.8 or higher
- Django 5.2.14
- Django REST Framework 3.17.1

## Installation & Setup

### 1. Clone or Navigate to the Project

```bash
cd c:\Users\Ipro_Python\Documents\Airtribe-learning\Projects\eventHub
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv .virtual

# Activate virtual environment (Windows)
.virtual\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

## Running the Project

### Start the Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

### Access the Admin Panel

Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

### Access the API

Navigate to `http://127.0.0.1:8000/api/` to view the browsable API.

## API Endpoints

### Events Management

#### 1. List All Events
- **URL**: `/api/events/`
- **Method**: `GET`
- **Description**: Retrieve all events with optional filtering
- **Query Parameters**:
  - `status` (optional): Filter by status (`upcoming`, `ongoing`, `completed`, `cancelled`)
  - `venue` (optional): Filter by venue (case-insensitive search)
- **Response**: List of event objects
- **Example**:
  ```
  GET /api/events/?status=upcoming&venue=NYC
  ```

#### 2. Create Event
- **URL**: `/api/events/`
- **Method**: `POST`
- **Description**: Create a new event
- **Request Body**:
  ```json
  {
    "title": "Python Conference 2026",
    "venue": "New York Convention Center",
    "date": "2026-06-15",
    "total_seats": 500,
    "available_seats": 500,
    "status": "upcoming"
  }
  ```
- **Response**: Created event object with ID

#### 3. Get Event Details
- **URL**: `/api/events/{id}/`
- **Method**: `GET`
- **Description**: Retrieve a specific event by ID
- **Response**: Event object with reservation count
- **Example**:
  ```
  GET /api/events/1/
  ```

#### 4. Update Event
- **URL**: `/api/events/{id}/`
- **Method**: `PUT` (full update) or `PATCH` (partial update)
- **Description**: Update event information
- **Request Body**: Event fields to update
- **Response**: Updated event object
- **Example**:
  ```
  PATCH /api/events/1/
  {
    "status": "ongoing"
  }
  ```

#### 5. Delete Event
- **URL**: `/api/events/{id}/`
- **Method**: `DELETE`
- **Description**: Delete an event
- **Response**: 204 No Content

---

### Reservations Management

#### 1. List All Reservations
- **URL**: `/api/reservations/`
- **Method**: `GET`
- **Description**: Retrieve all reservations with optional filtering
- **Query Parameters**:
  - `event_id` (optional): Filter reservations by event ID
- **Response**: List of reservation objects
- **Example**:
  ```
  GET /api/reservations/?event_id=1
  ```

#### 2. Create Reservation
- **URL**: `/api/reservations/`
- **Method**: `POST`
- **Description**: Create a new reservation
- **Request Body**:
  ```json
  {
    "event": 1,
    "attendee_name": "John Doe",
    "attendee_email": "john@example.com",
    "seats_reserved": 2
  }
  ```
- **Validation Rules**:
  - Must reserve at least 1 seat
  - Event status must be `upcoming` or `ongoing`
  - Seats requested cannot exceed available seats
- **Response**: Created reservation object

#### 3. Get Reservation Details
- **URL**: `/api/reservations/{id}/`
- **Method**: `GET`
- **Description**: Retrieve a specific reservation by ID
- **Response**: Reservation object
- **Example**:
  ```
  GET /api/reservations/1/
  ```

#### 4. Update Reservation
- **URL**: `/api/reservations/{id}/`
- **Method**: `PUT` (full update) or `PATCH` (partial update)
- **Description**: Update reservation details
- **Request Body**: Reservation fields to update (read-only: status, created_at)
- **Response**: Updated reservation object

#### 5. Delete Reservation
- **URL**: `/api/reservations/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a reservation
- **Response**: 204 No Content

#### 6. Cancel Reservation (Custom Action)
- **URL**: `/api/reservations/{id}/cancel/`
- **Method**: `POST`
- **Description**: Cancel an existing reservation and restore seats to the event
- **Response**: Updated reservation object with `status: cancelled`
- **Error Handling**: Returns error if reservation is already cancelled
- **Example**:
  ```
  POST /api/reservations/1/cancel/
  ```

---

## Usage Examples

### Example 1: Create an Event and Make a Reservation

#### Step 1: Create an Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Meetup",
    "venue": "Downtown Hall",
    "date": "2026-06-01",
    "total_seats": 100,
    "available_seats": 100,
    "status": "upcoming"
  }'
```

#### Step 2: Reserve Seats
```bash
curl -X POST http://127.0.0.1:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -d '{
    "event": 1,
    "attendee_name": "Jane Smith",
    "attendee_email": "jane@example.com",
    "seats_reserved": 5
  }'
```

#### Step 3: Check Event Availability
```bash
curl http://127.0.0.1:8000/api/events/1/
```

#### Step 4: Cancel Reservation
```bash
curl -X POST http://127.0.0.1:8000/api/reservations/1/cancel/
```

### Example 2: Filter Events

```bash
# Get all upcoming events
curl http://127.0.0.1:8000/api/events/?status=upcoming

# Get events at a specific venue
curl http://127.0.0.1:8000/api/events/?venue=NYC

# Combine filters
curl http://127.0.0.1:8000/api/events/?status=upcoming&venue=Downtown
```

### Example 3: Filter Reservations by Event

```bash
# Get all reservations for event ID 1
curl http://127.0.0.1:8000/api/reservations/?event_id=1
```

---

## Models

### Event Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `title` | String (200) | Event title |
| `venue` | String (200) | Event location |
| `date` | Date | Event date |
| `total_seats` | Positive Integer | Total available seats |
| `available_seats` | Positive Integer | Currently available seats |
| `status` | Choice | Event status: `upcoming`, `ongoing`, `completed`, `cancelled` |
| `created_at` | DateTime | Creation timestamp (auto) |
| `reservations_count` | Integer | Count of confirmed reservations (read-only) |

### Reservation Model

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `event` | ForeignKey | Reference to Event |
| `attendee_name` | String (200) | Name of the attendee |
| `attendee_email` | Email | Email of the attendee |
| `seats_reserved` | Positive Integer | Number of seats reserved |
| `status` | Choice | Reservation status: `confirmed`, `cancelled` |
| `created_at` | DateTime | Creation timestamp (auto) |

---

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Example Error Response
```json
{
  "non_field_errors": [
    "Cannot reserve seats for a completed event."
  ]
}
```

---

## Project Structure

```
eventHub/
├── app/
│   ├── models.py           # Event and Reservation models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets for API endpoints
│   ├── url.py              # App URL routing
│   ├── admin.py            # Django admin configuration
│   └── migrations/         # Database migrations
├── eventHub/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Project URL configuration
│   └── wsgi.py             # WSGI application
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── db.sqlite3             # SQLite database
```

---

## Troubleshooting

### Virtual Environment Not Activating
Make sure you're in the correct project directory and use the full path to the activate script.

### Port 8000 Already in Use
Use a different port:
```bash
python manage.py runserver 8001
```

### Migration Errors
Reset the database (development only):
```bash
python manage.py migrate app zero
python manage.py migrate
```

---

## License

This project is part of the Airtribe learning program.

---

## Support

For issues or questions, please refer to the Django REST Framework documentation: https://www.django-rest-framework.org/
