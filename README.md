# 📚 Bookstore API with Flask & SQLite

A full-stack Bookstore Application with:

- **Backend**: Flask, SQLite, JWT authentication
- **Frontend**: HTML/CSS (templates/index.html), Bootstrap
- **Containerization**: Docker & Docker Compose
- **Testing**: Python unittest, Coverage report

---

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

---

## 📬 API Endpoints

### Authentication

| Endpoint       | Method | Description                    |
| -------------- | ------ | ------------------------------ |
| `/signup`      | POST   | Register new user             |
| `/login`       | POST   | Login, sets HTTP-only cookie  |
| `/logout`      | POST   | Logout, clears cookie         |

#### Request Body (JSON)

```json
{
  "email": "user@example.com",
  "password": "YourPassword"
}
```

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

---

## 🧪 Testing & Coverage

```bash
# Run tests
python3 -m unittest test_app.py

# Coverage
pip install coverage
coverage run -m unittest test_app.py
coverage report -m
```

**Coverage Report**:

```
Name          Stmts   Miss  Cover
---------------------------------
app.py          183     24    87%
test_app.py      69      1    99%
TOTAL           252     25    90%
```

---

## 🐳 Docker

### Build & Run (Docker)

```bash
docker build -t bookstore-api .
docker run -p 5000:5000 bookstore-api
```

### Docker Compose

```bash
docker-compose up --build
```

---

