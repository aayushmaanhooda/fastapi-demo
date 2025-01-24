from fastapi import FastAPI, HTTPException, Path, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str 
    author: str 
    description: str 
    rating: int

    
    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

'''
we just saw raw model and basic approach in our project2,
lets introduce pydantic and its powefull feature which helps in data validation data modelling
data parsing and efficient error handling
'''

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not needed on create", default= None) 
    title: str = Field(min_length =3)
    author: str =  Field(min_length=1)
    description: str = Field(min_length = 2, max_length = 10)
    rating: int = Field(gt=-1, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title:": "A New Book",
                "author": "codingwithhtoby",
                "description": "A new description of a book",
                "rating": 5
            }
        }
    }



    def __str__(self):
        return f"BookRequest(title='{self.title}', author='{self.author}', rating={self.rating})"

    def __repr__(self):
        return (
            f"BookRequest(id={self.id}, title='{self.title}', "
            f"author='{self.author}', description='{self.description}', rating={self.rating})"
        )

books=[
    Book(1, 'Computer Science Pro', 'Codingwiththrophy','A very nice book!', 4),
    Book(2, 'Be fast with FastAPI', 'Codingwiththrophy','A very nice book!', 4),
    Book(3, 'Master Endpoints', 'Codingwiththrophy','A very nice book!', 3),
    Book(4, 'HP1', 'J.K rolling','A very nice book!', 5),
    Book(5, 'HP2', 'J.K rolling','A very nice book!', 5),
    Book(5, 'HP3', 'J.K rolling','A very nice book!', 5),
    Book(6, 'Nueral Nets', 'Author bhai','A very nice book!', 3),
    Book(7, 'Nueral Nets2.0', 'Author bhai2','A very nice book! ig', 3),
    Book(8, 'Nueral Nets', 'Author bhai','A very nice book!', 2),
]

@app.get("/books", status_code = status.HTTP_2OO_OK)
async def read_all_books(response_model = List[Book]):
    return books

@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(gt=0)):
    for book in books:
        if book.id == book_id:
            return {
                "Message" : f"Book Found with {book_id}",
                "Book": book
            }
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@app.get("/books/")
async def get_by_rating(rate: int = Query(gt=0, lt=6)):
    rating_obj = []
    for book in books:
        if book.rating == rate:
            rating_obj.append(book)
    if rating_obj:
        return {
            "message": f"These are books with rating {rate}",
            "Books": rating_obj
        }
    raise HTTPException(status_code=404, detail= f"No book found with rating {rate}") 




@app.post("/books/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_id(new_book))
    return {
        "Message": "Created Successfully",
        "book": book_request
    }

def find_id(book: Book):
    if len(books) > 0:
        book.id = Book[-1].id +1
    else:
        book.id = 1
    return book


@app.put("/books/update")
async def update_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book
    return {
        "Message": "Updated Successfully",
        "Book": books[i]
    }

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(books)):
        if books[i].id == book_id:
            item = books.pop(i)
            break
    return {
        "Message" : f"Item deleted with id {book_id}",
        "Deleted Book": item
    }


'''
200 ok response
201 created successfully
204 used in put and delete as we dont return anything just made changes 
    or say success with no body
'''