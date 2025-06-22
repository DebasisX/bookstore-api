# Bookstore API with Flask & SQLite

<<<<<<< HEAD
A full-stack Bookstore Application with:

- **Backend**: Flask, SQLite, JWT authentication
- **Frontend**: HTML/CSS (templates/index.html), Bootstrap
- **Containerization**: Docker & Docker Compose
- **Testing**: Python unittest, Coverage report
=======
A simple RESTful API for a Bookstore Application built with Flask and SQLite.  
This project demonstrates user signup/login (JWT-based authentication) and CRUD operations on books with filtering, pagination, and sorting.

## Table of Contents
>>>>>>> 3abf85c (added test and report)

- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)
- [Running Tests](#running-tests)
- [Dockerization](#dockerization)

<<<<<<< HEAD
## 🗂 Project Structure

```
.
├── app.py
├── templates/
│   └── index.html
├── test_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)

### Backend Setup

```bash
git clone <repo_url>
cd bookstore-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize and run
python app.py
```

By default, the server runs at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Frontend

The frontend is served from `templates/index.html`. It uses Bootstrap for styling. Simply navigate to the root URL:

[http://127.0.0.1:5000](http://127.0.0.1:5000) to view the UI.
=======
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

3. **Install the dependencies:**

    pip install flask pyjwt werkzeug

4. **Run the application:**

    python app.py

The server will start at http://127.0.0.1:5000!

# API Endpoints
Authentication

# POST /signup
Request Body:
>>>>>>> 3abf85c (added test and report)

{
  "email": "user@example.com",
  "password": "YourPassword"
}

<<<<<<< HEAD
## 📬 API Endpoints

### Authentication

| Endpoint       | Method | Description                    |
| -------------- | ------ | ------------------------------ |
| `/signup`      | POST   | Register new user             |
| `/login`       | POST   | Login, sets HTTP-only cookie  |
| `/logout`      | POST   | Logout, clears cookie         |

#### Request Body (JSON)

```json
=======
# POST /login
Request Body:

>>>>>>> 3abf85c (added test and report)
{
  "email": "user@example.com",
  "password": "YourPassword"
}
Books (Protected - JWT token required in the Authorization header as Bearer <token>)

<<<<<<< HEAD
### Books (Protected, Cookie-based JWT)

| Endpoint              | Method | Description                             |
| --------------------- | ------ | --------------------------------------- |
| `/books`              | POST   | Create new book                         |
| `/books`              | GET    | List books (filter, search, sort, page) |
| `/books/<id>`         | GET    | Get single book by ID                   |
| `/books/<id>`         | PUT    | Update book by ID                       |
| `/books/<id>`         | DELETE | Delete book by ID                       |

#### Query Parameters for `GET /books`

- `author`: partial match
- `category`: partial match
- `rating`: exact match
- `search`: title partial match
- `sortBy`: `price` or `rating`
- `order`: `asc` | `desc` (default `asc`)
- `page`: page number (default 1)
- `perPage`: items per page (default 10)

---

## 🛠 Examples (cURL)

### Sign Up

```bash
curl -X POST http://127.0.0.1:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"mypassword"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"mypassword"}' \
  -c cookies.txt
```

### Create Book

```bash
curl -X POST http://127.0.0.1:5000/books \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"1984","author":"Orwell","category":"Dystopia","price":9.99,"rating":4.5,"publishedDate":"1949-06-08"}'
```

### List Books with Pagination & Sorting

```bash
curl -X GET "http://127.0.0.1:5000/books?sortBy=price&order=desc&page=1&perPage=5" \
  -b cookies.txt
```
=======
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
>>>>>>> 3abf85c (added test and report)

# List Books with Filtering & Pagination

<<<<<<< HEAD
## 🧪 Testing & Coverage

```bash
# Run tests
python3 -m unittest test_app.py

# Coverage
pip install coverage
coverage run -m unittest test_app.py
coverage report -m
```

✅ **Unit Tests**  
- `test_unit_signup_db_error`: Uses `unittest.mock` to simulate an `sqlite3.IntegrityError`, covering error handling in user signup logic.  

✅ **Integration Tests**  
- Full flow tested via `test_api_book_crud_operations`:  
  - Signup  
  - Login  
  - Create Book  
  - Read All Books (List)  
  - Read Book by ID  
  - Update Book  
  - Delete Book  
  - Confirm Deletion  
- These interact with a real temporary SQLite DB.  

✅ **API Tests**  
- `/signup` and `/login` tested (`test_api_signup_and_login`)  
- `/books` endpoints tested end-to-end (`test_api_book_crud_operations`)  
- Unauthorized access tested (`test_book_creation_without_token`)  

🔒 **Auth Handling**
- Token is passed via **Cookie**, consistent with your `@tokenRequired` decorator.

🧪 **Testing Framework**
- Tests are written using the `unittest` module as specified.

🎯 **Coverage**
- Covers both **happy** (success) and **unhappy** (failure) paths.

**Coverage Report**:

```
Name          Stmts   Miss  Cover
---------------------------------
app.py          183     24    87%
test_app.py      69      1    99%
TOTAL           252     25    90%
```
=======
curl -X GET -H "Authorization: Bearer <token>" \
"http://127.0.0.1:5000/books?sortBy=price&order=asc&page=1&perPage=10"

# Running Tests
Basic unit tests have been provided in test_app.py using Python's unittest module.
To run the tests, simply execute:

python -m unittest test_app.py
>>>>>>> 3abf85c (added test and report)

# Dockerization
A Dockerfile is provided to containerize the application. To build and run the Docker container:

<<<<<<< HEAD
## 🐳 Docker

### Build & Run (Docker)

```bash
docker build -t bookstore-api .
docker run -p 5000:5000 bookstore-api
```

### Docker Compose

```bash
=======
# Build the Docker image:

docker build -t bookstore-api .
or using compose
>>>>>>> 3abf85c (added test and report)
docker-compose up --build

<<<<<<< HEAD
---

=======

# Run the Docker container:

docker run -p 5000:5000 bookstore-api
or if using compose 
docker-compose up 
The API will then be available at http://127.0.0.1:5000.

Example RUN is shown in the test.txt!
>>>>>>> 3abf85c (added test and report)
