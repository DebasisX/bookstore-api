from flask import Flask, request, jsonify, g
import sqlite3
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

""" 
Used camelCase for professionalism and code formatting using black
and boilerplate code snippets from my other projects 
"""

# config load from .env, i have used sample.
DATABASE = "/data/bookstore.db"  # making it persistent
SECRET_KEY = "secret_key"

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


# connect to the db
def getDb():
    dbPath = app.config.get("DATABASE", DATABASE)
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(dbPath)
        db.row_factory = sqlite3.Row
    return db


# initialize db, creating the tables
def initDb():
    with app.app_context():
        db = getDb()
        cursor = db.cursor()
        # users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT
            )
        """
        )
        # books table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                category TEXT,
                price REAL,
                rating REAL,
                published_date TEXT
            )
        """
        )
        db.commit()


@app.teardown_appcontext  # this is to close the connection after a call is handled
def closeConnection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# JWT auth boilerplate code!
def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            authHeader = request.headers["Authorization"]
            if authHeader.startswith("Bearer "):
                token = authHeader.split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            currentUserId = data["userId"]
        except Exception as e:
            print(e)
            return jsonify({"message": "Token is invalid!"}), 401
        return f(currentUserId, *args, **kwargs)

    return decorated


# signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    hashedPassword = generate_password_hash(password)
    try:
        db = getDb()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)", (email, hashedPassword)
        )
        db.commit()
        return jsonify({"message": "User created successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "User already exists."}), 409


# login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    db = getDb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    # verification of password, JWT with username
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401
    # expiration set to 24 hrs
    token = jwt.encode(
        {
            "userId": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return jsonify({"token": token})


# new book
@app.route("/books", methods=["POST"])
@tokenRequired
def createBook(currentUserId):
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    category = data.get("category")
    price = data.get("price")
    rating = data.get("rating")
    publishedDate = data.get("publishedDate")

    if not title or not author:
        return jsonify({"message": "Title and author are required"}), 400
    # insertion of the book in db
    db = getDb()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, author, category, price, rating, published_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (title, author, category, price, rating, publishedDate),
    )
    db.commit()
    bookId = cursor.lastrowid  # last id to return back what was inserted
    return jsonify({"message": "Book created", "bookId": bookId}), 201


# get all books with filtering, search, pagination, and sorting
@app.route("/books", methods=["GET"])
@tokenRequired
def getBooks(currentUserId):
    queryParams = request.args
    author = queryParams.get("author")
    category = queryParams.get("category")
    rating = queryParams.get("rating")
    search = queryParams.get("search")
    sortBy = queryParams.get("sortBy")
    order = queryParams.get("order", "asc")
    page = int(queryParams.get("page", 1))
    perPage = int(queryParams.get("perPage", 10))

    baseQuery = "SELECT * FROM books WHERE 1=1"  # evaluates to true always so can add AND conditions, I learnt this in SQL injection CS50 Lecture 7 Harvard!
    params = []  # to add to the base
    if author:
        baseQuery += " AND author LIKE ?"
        params.append(f"%{author}%")
    if category:
        baseQuery += " AND category LIKE ?"
        params.append(f"%{category}%")
    if rating:
        baseQuery += " AND rating = ?"
        params.append(rating)
    if search:
        baseQuery += " AND title LIKE ?"
        params.append(f"%{search}%")
    if sortBy in ["price", "rating"]:
        baseQuery += f" ORDER BY {sortBy} {'ASC' if order.lower() == 'asc' else 'DESC'}"
    else:
        baseQuery += " ORDER BY id ASC"
    # Example: page 3 with 10 per page -> skip first 20 books.
    offset = (page - 1) * perPage  # skips record
    baseQuery += " LIMIT ? OFFSET ?"
    params.extend([perPage, offset])

    db = getDb()
    cursor = db.cursor()
    cursor.execute(baseQuery, params)
    books = cursor.fetchall()

    booksList = []
    for book in books:
        booksList.append(
            {
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "category": book["category"],
                "price": book["price"],
                "rating": book["rating"],
                "publishedDate": book["published_date"],
            }
        )

    return jsonify({"books": booksList})


# get book by ID
@app.route("/books/<int:bookId>", methods=["GET"])
@tokenRequired
def getBookById(currentUserId, bookId):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (bookId,))
    book = cursor.fetchone()
    if not book:
        return jsonify({"message": "Book not found"}), 404

    bookData = {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "category": book["category"],
        "price": book["price"],
        "rating": book["rating"],
        "publishedDate": book["published_date"],
    }
    return jsonify(bookData)


# update book by ID
@app.route("/books/<int:bookId>", methods=["PUT"])
@tokenRequired
def updateBookById(currentUserId, bookId):
    data = request.get_json()
    db = getDb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (bookId,))
    book = cursor.fetchone()
    if not book:
        return jsonify({"message": "Book not found"}), 404

    title = data.get("title", book["title"])
    author = data.get("author", book["author"])
    category = data.get("category", book["category"])
    price = data.get("price", book["price"])
    rating = data.get("rating", book["rating"])
    publishedDate = data.get("publishedDate", book["published_date"])
    # i don't need to explain this
    cursor.execute(
        """
        UPDATE books SET title = ?, author = ?, category = ?, price = ?, rating = ?, published_date = ?
        WHERE id = ?
    """,
        (title, author, category, price, rating, publishedDate, bookId),
    )
    db.commit()
    return jsonify({"message": "Book updated"})


# delete book by ID
@app.route("/books/<int:bookId>", methods=["DELETE"])
@tokenRequired
def deleteBookById(currentUserId, bookId):  # passing currentUserId because of JWT
    db = getDb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (bookId,))
    book = cursor.fetchone()
    if not book:
        return jsonify({"message": "Book not found"}), 404
    # Nor this
    cursor.execute("DELETE FROM books WHERE id = ?", (bookId,))
    db.commit()
    return jsonify({"message": "Book deleted"})


if __name__ == "__main__":
    initDb()
    app.run(host="0.0.0.0", port=5000, debug=True)

# code formatted using black app.py
