# Gamma AI - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### Register User

**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Login

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Presentation Endpoints

### Generate Presentation

**POST** `/presentations/generate`

Generate a new presentation using AI.

**Request Body:**
```json
{
  "prompt": "Artificial Intelligence in Healthcare",
  "slides_count": 8,
  "language": "English",
  "theme": "dialogue",
  "text_amount": "concise",
  "ai_model": "gemini"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Presentation generated successfully"
}
```

---

For complete API documentation, see the README.md file.
