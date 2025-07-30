from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Atomic Habits", "author": "James Clear"},
    {"id": 2, "title": "The Alchemist", "author": "Paulo Coelho"},
    {"id": 3, "title": "Deep Work", "author": "Cal Newport"}
]

@app.route('/')
def home():
    return "Book API is running. Visit /books to see the list."

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else ("Book not found", 404)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = {
        "id": max(b["id"] for b in books) + 1,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return ("Book not found", 404)
    data = request.json
    book.update({
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"])
    })
    return jsonify(book)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return ("", 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
