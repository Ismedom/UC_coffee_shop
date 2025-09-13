---
# UC Coffee Shop ☕

A FastAPI project for managing users, roles, and permissions in a coffee shop system.
---

## 🔧 Setup & Installation

### 1. Create Virtual Environment

```bash
# Linux / macOS
python3 -m venv venv

# Windows
python -m venv venv
```

### 2. Activate the Virtual Environment

- **Linux / macOS**

  ```bash
  source venv/bin/activate
  ```

- **Windows (Command Prompt)**

  ```cmd
  venv\Scripts\activate.bat
  ```

- **Windows (PowerShell)**

  ```powershell
  venv\Scripts\Activate.ps1
  ```

---

### 3. Configure Environment Variables

Create a `.env` file in the project root.
Copy the contents of `.env.local` and fill in the missing values (e.g., database URL, secret key, etc.).

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the Project

Start the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The app will be available at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive API docs:

- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🌱 Database Seeding

### Seed Users

```bash
python -m app.database.seed
```

### Seed Roles & Permissions

```bash
python -m app.database.role_permission
```

### Assign Roles to Permissions

```bash
python -m app.database.assign
```

---
