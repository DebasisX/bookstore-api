# 📚 Bookstore API with Flask & SQLite

A simple RESTful API for a Bookstore Application built with Flask and SQLite.  
This project demonstrates user signup/login (JWT-based authentication) and CRUD operations on books with filtering, pagination, and sorting.

## Table of Contents

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)
- [Running Tests](#running-tests)
- [Dockerization](#dockerization)

## Features

- **User Authentication**: 
  - Sign up a new user.
  - Login and receive a JWT token.
- **Books API**:
  - Create, get, update, and delete books.
  - Filtering by author, category, rating.
  - Search by title (partial match).
  - Pagination and sorting (by price or rating).
- **Error Handling**:  
  - Proper HTTP status codes for errors and validations.
- **Unit Tests**: Basic tests covering signup and login endpoints.
- **Docker Support**: Containerized application.

## Setup Instructions

1. **Clone the repository (if using GitHub) or download the project folder.**

2. **Create a virtual environment (optional):**

   python3 -m venv venv
   source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

    pip install flask pyjwt werkzeug

4. **Run the application:**

    python app.py

The server will start at http://127.0.0.1:5000!

# API Endpoints
Authentication

# POST /signup
Request Body:

{
  "email": "user@example.com",
  "password": "YourPassword"
}

# POST /login
Request Body:

{
  "email": "user@example.com",
  "password": "YourSecurePassword"
}
Books (Protected - JWT token required in the Authorization header as Bearer <token>)

### Example Requests (using cURL)

# Sign Up

curl -X POST -H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "YourSecurePassword"}' \
http://127.0.0.1:5000/signup

# Login

curl -X POST -H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "YourSecurePassword"}' \
http://127.0.0.1:5000/login

# Create a Book (Replace <token> with your JWT)

curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImV4cCI6MTc0NDIzMjAxN30.DC2WZTAAm6GmErAN0db8vYDs8RLLadEuhkQ9kD6Rcas" \
-d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic", "price": 10.99, "rating": 4.3, "publishedDate": "1925-04-10"}' \
http://127.0.0.1:5000/books

# List Books with Filtering & Pagination

curl -X GET -H "Authorization: Bearer <token>" \
"http://127.0.0.1:5000/books?sortBy=price&order=asc&page=1&perPage=10"

# Running Tests
Basic unit tests have been provided in test_app.py using Python's unittest module.
To run the tests, simply execute:

python -m unittest test_app.py

# Dockerization
A Dockerfile is provided to containerize the application. To build and run the Docker container:

# Build the Docker image:

docker build -t bookstore-api .
or using compose
docker-compose up --build


# Run the Docker container:

docker run -p 5000:5000 bookstore-api
or if using compose 
docker-compose up 
The API will then be available at http://127.0.0.1:5000.

Example RUN is shown in the test.txt!
[Download Updated README.md](sandbox:/mnt/data/README.md)

## 🧪 API Testing with Keploy

All API tests were generated using the [Keploy Chrome Extension](https://github.com/keploy/extension) and executed via the [Keploy Dashboard](https://app.keploy.io).

✅ Test Suite: All tests passed  
📸 Screenshots:

![Keploy Passed Tests](./Screenshot%20from%202025-06-28%2000-59-51.png)

## 🧪 Keploy API Testing & CI/CD
✅ Recorded real API calls using:

keploy record -c "python3 app.py" --record-timer 60

🔁 Replayed tests using:
keploy test -c "python3 app.py" --delay 5
🧪 Results: 2 Passed / 4 Total

📊 Coverage: 32% (coverage.json)

⚙️ GitHub Actions Integration
Keploy tests run automatically on every push via GitHub Actions:

![Keploy Test Result](./keploy_test.png)
