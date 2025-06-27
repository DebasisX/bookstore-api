from flask import Flask, request, jsonify, g, make_response, send_from_directory, redirect, render_template # Added render_template
import sqlite3
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "bookstore.db"
SECRET_KEY = "secret_key"

# Initialize Flask app, pointing to the 'templates' folder for templates
# and 'static' for static files (though you don't have a static folder in this example yet)
app = Flask(__name__) # Removed template_folder='templates', as this is the default
app.config["SECRET_KEY"] = SECRET_KEY

# Connect to SQLite
def getDb():
    dbPath = app.config.get("DATABASE", DATABASE)
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(dbPath)
        db.row_factory = sqlite3.Row
    return db

# Initialize DB
def initDb():
    with app.app_context():
        db = getDb()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                category TEXT,
                price REAL,
                rating REAL,
                published_date TEXT
            )
        """)
        db.commit()

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Secure token decorator using cookie
def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
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

# Signup
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

# Login with cookie
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
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "userId": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    resp = make_response(jsonify({"message": "Login successful"}))
    resp.set_cookie(
        "token", token,
        httponly=True,
        secure=False,
        samesite='Strict'
    )
    return resp

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logged out"}))
    resp.set_cookie("token", "", expires=0)
    return resp

# Create book
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
    return jsonify({"message": "Book created", "bookId": cursor.lastrowid}), 201

# Get books
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

    baseQuery = "SELECT * FROM books WHERE 1=1"
    params = []
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

    offset = (page - 1) * perPage
    baseQuery += " LIMIT ? OFFSET ?"
    params.extend([perPage, offset])

    db = getDb()
    cursor = db.cursor()
    cursor.execute(baseQuery, params)
    books = cursor.fetchall()

    booksList = [
        {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "category": book["category"],
            "price": book["price"],
            "rating": book["rating"],
            "publishedDate": book["published_date"],
        } for book in books
    ]

    return jsonify({"books": booksList})

# Book by ID
@app.route("/books/<int:bookId>", methods=["GET"])
@tokenRequired
def getBookById(currentUserId, bookId):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (bookId,))
    book = cursor.fetchone()
    if not book:
        return jsonify({"message": "Book not found"}), 404

    return jsonify({
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "category": book["category"],
        "price": book["price"],
        "rating": book["rating"],
        "publishedDate": book["published_date"],
    })

# Update book
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

    cursor.execute(
        """
        UPDATE books SET title = ?, author = ?, category = ?, price = ?, rating = ?, published_date = ?
        WHERE id = ?
        """,
        (title, author, category, price, rating, publishedDate, bookId),
    )
    db.commit()
    return jsonify({"message": "Book updated"})

# Delete book
@app.route("/books/<int:bookId>", methods=["DELETE"])
@tokenRequired
def deleteBookById(currentUserId, bookId):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (bookId,))
    book = cursor.fetchone()
    if not book:
        return jsonify({"message": "Book not found"}), 404

    cursor.execute("DELETE FROM books WHERE id = ?", (bookId,))
    db.commit()
    return jsonify({"message": "Book deleted"})

# Serve frontend
@app.route('/')
def serveIndex():
    # Corrected: Render the template directly, don't redirect to it as a static file
    return render_template('index.html')

if __name__ == "__main__":
    initDb()
    app.run(host="0.0.0.0", port=5050, debug=True)
