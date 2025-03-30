from tkinter.font import names

from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'Science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'History'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'Art'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'science'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'Philosophy'}
]
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/author_books/")
async def author_books_query_param(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(update_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)

@app.get("/books/author_books/{author_name}")
async def author_books_path_param(author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            books_to_return.append(book)
    return books_to_return

