# College ERP – Backend API 🎓

A scalable and production-ready backend for a **College ERP (Enterprise Resource Planning) System** built using FastAPI and SQLAlchemy 2.0.

This project is designed to manage core academic and administrative workflows such as students, faculty, courses, departments, and more.

---

## 🚀 Tech Stack

- Framework: FastAPI
- ORM: SQLAlchemy (2.0 style)
- Migrations (Planned): Alembic
- ASGI Server: Uvicorn
- Environment Management: python-dotenv
- Database: PostgreSQL 

---

## 📂 Project Structure

```
backend/
│
├── app/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy Base + Naming Conventions
│   │   ├── database.py      # Engine configuration
|   │   ├── models.py        # Database Schema Declared
│   │
|   ├── routes
|   │   ├── __init__.py
│   |
|   ├── schemas
|   │   ├── __init__.py
|   |
│   ├── utils/
|       ├── __init__.py
│       ├── constants.py     # Application constants
│   
├── main.py              # FastAPI entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Features (Planned & In Progress)

- Student Management
- Faculty Management
- Course & Department Management
- Role-based Authentication
- Attendance Tracking
- Result Management
- RESTful API architecture
- Scalable database design
- Clean modular structure

---

## 🏗️ Architecture Overview

### 🔹 FastAPI Application

The application entry point is defined in:

```
app/main.py
```

It initializes:

- FastAPI instance
- Database engine
- Table creation via:

```python
Base.metadata.create_all(bind=engine)
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd backend
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv psycopg2-binary
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file inside `app/`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/college_erp
```

---

### 5️⃣ Run the Server

From the project root (`backend/`):

```bash
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Health Check

**GET /**

Response:

```json
{
  "message": "ERP System API is running!"
}
```

---

## 🧠 Design Principles

- Clean architecture
- Separation of concerns
- Scalable folder structure
- SQLAlchemy 2.0 modern patterns
- Production-safe constraint naming
- Environment-based configuration

---



