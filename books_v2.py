from typing import Optional
from fastapi import FastAPI ,Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title = 'id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Coding With Roby',
                'description': 'A new book',
                'rating': 5,
                'published_date': 2025,
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'CodingWithRoby', 'A very nice book on computer science!', 5, 1998),
    Book(2, 'The Art of Programming', 'Jane Doe', 'A comprehensive guide to programming.', 4, 2020),
    Book(3, 'History of the World', 'John Smith', 'An in-depth history book covering ancient civilizations.', 3, 2021),
    Book(4, 'Philosophy for Beginners', 'Emily White', 'An easy-to-understand introduction to philosophy.', 5, 2005),
    Book(5, 'The Science of Everything', 'Dr. Richard Brown', 'A book that explains complex scientific principles in simple terms.', 4, 2012),
    Book(6, 'The Secrets of Art', 'Anna Green', 'A detailed guide to mastering the basics of art and creativity.', 5, 2007),
    Book(7, 'Technology in the Modern World', 'Samuel Black', 'Exploring how technology is shaping the world today.', 4, 2013),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed: raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            book_changed = True
            BOOKS.pop(i)
            break
    if not book_changed: raise HTTPException(status_code=404, detail="Book not found")