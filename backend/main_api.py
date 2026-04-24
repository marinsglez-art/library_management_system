import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Library.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Library API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Author", "description": "Operations for Author entities"},
        {"name": "Author Relationships", "description": "Manage Author relationships"},
        {"name": "Library", "description": "Operations for Library entities"},
        {"name": "Library Relationships", "description": "Manage Library relationships"},
        {"name": "Library Methods", "description": "Execute Library methods"},
        {"name": "Book", "description": "Operations for Book entities"},
        {"name": "Book Relationships", "description": "Manage Book relationships"},
        {"name": "Book Methods", "description": "Execute Book methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Library API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["author_count"] = database.query(Author).count()
    stats["library_count"] = database.query(Library).count()
    stats["book_count"] = database.query(Book).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Author functions
#
############################################

@app.get("/author/", response_model=None, tags=["Author"])
def get_all_author(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Author)
        author_list = query.all()

        # Serialize with relationships included
        result = []
        for author_item in author_list:
            item_dict = author_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            book_list = database.query(Book).join(books_1, Book.id == books_1.c.books).filter(books_1.c.authors == author_item.id).all()
            item_dict['books'] = []
            for book_obj in book_list:
                book_dict = book_obj.__dict__.copy()
                book_dict.pop('_sa_instance_state', None)
                item_dict['books'].append(book_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Author).all()


@app.get("/author/count/", response_model=None, tags=["Author"])
def get_count_author(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Author entities"""
    count = database.query(Author).count()
    return {"count": count}


@app.get("/author/paginated/", response_model=None, tags=["Author"])
def get_paginated_author(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Author entities"""
    total = database.query(Author).count()
    author_list = database.query(Author).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": author_list
        }

    result = []
    for author_item in author_list:
        book_ids = database.query(books_1.c.books).filter(books_1.c.authors == author_item.id).all()
        item_data = {
            "author": author_item,
            "book_ids": [x[0] for x in book_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/author/search/", response_model=None, tags=["Author"])
def search_author(
    database: Session = Depends(get_db)
) -> list:
    """Search Author entities by attributes"""
    query = database.query(Author)


    results = query.all()
    return results


@app.get("/author/{author_id}/", response_model=None, tags=["Author"])
async def get_author(author_id: int, database: Session = Depends(get_db)) -> Author:
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    book_ids = database.query(books_1.c.books).filter(books_1.c.authors == db_author.id).all()
    response_data = {
        "author": db_author,
        "book_ids": [x[0] for x in book_ids],
}
    return response_data



@app.post("/author/", response_model=None, tags=["Author"])
async def create_author(author_data: AuthorCreate, database: Session = Depends(get_db)) -> Author:

    if author_data.books:
        for id in author_data.books:
            # Entity already validated before creation
            db_book = database.query(Book).filter(Book.id == id).first()
            if not db_book:
                raise HTTPException(status_code=404, detail=f"Book with ID {id} not found")

    db_author = Author(
        birth=author_data.birth,        name=author_data.name        )

    database.add(db_author)
    database.commit()
    database.refresh(db_author)


    if author_data.books:
        for id in author_data.books:
            # Entity already validated before creation
            db_book = database.query(Book).filter(Book.id == id).first()
            # Create the association
            association = books_1.insert().values(authors=db_author.id, books=db_book.id)
            database.execute(association)
            database.commit()


    book_ids = database.query(books_1.c.books).filter(books_1.c.authors == db_author.id).all()
    response_data = {
        "author": db_author,
        "book_ids": [x[0] for x in book_ids],
    }
    return response_data


@app.post("/author/bulk/", response_model=None, tags=["Author"])
async def bulk_create_author(items: list[AuthorCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Author entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_author = Author(
                birth=item_data.birth,                name=item_data.name            )
            database.add(db_author)
            database.flush()  # Get ID without committing
            created_items.append(db_author.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Author entities"
    }


@app.delete("/author/bulk/", response_model=None, tags=["Author"])
async def bulk_delete_author(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Author entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_author = database.query(Author).filter(Author.id == item_id).first()
        if db_author:
            database.delete(db_author)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Author entities"
    }

@app.put("/author/{author_id}/", response_model=None, tags=["Author"])
async def update_author(author_id: int, author_data: AuthorCreate, database: Session = Depends(get_db)) -> Author:
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    setattr(db_author, 'birth', author_data.birth)
    setattr(db_author, 'name', author_data.name)
    existing_book_ids = [assoc.books for assoc in database.execute(
        books_1.select().where(books_1.c.authors == db_author.id))]

    books_to_remove = set(existing_book_ids) - set(author_data.books)
    for book_id in books_to_remove:
        association = books_1.delete().where(
            (books_1.c.authors == db_author.id) & (books_1.c.books == book_id))
        database.execute(association)

    new_book_ids = set(author_data.books) - set(existing_book_ids)
    for book_id in new_book_ids:
        db_book = database.query(Book).filter(Book.id == book_id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
        association = books_1.insert().values(books=db_book.id, authors=db_author.id)
        database.execute(association)
    database.commit()
    database.refresh(db_author)

    book_ids = database.query(books_1.c.books).filter(books_1.c.authors == db_author.id).all()
    response_data = {
        "author": db_author,
        "book_ids": [x[0] for x in book_ids],
    }
    return response_data


@app.delete("/author/{author_id}/", response_model=None, tags=["Author"])
async def delete_author(author_id: int, database: Session = Depends(get_db)):
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    database.delete(db_author)
    database.commit()
    return db_author

@app.post("/author/{author_id}/books/{book_id}/", response_model=None, tags=["Author Relationships"])
async def add_books_to_author(author_id: int, book_id: int, database: Session = Depends(get_db)):
    """Add a Book to this Author's books relationship"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if relationship already exists
    existing = database.query(books_1).filter(
        (books_1.c.authors == author_id) &
        (books_1.c.books == book_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = books_1.insert().values(authors=author_id, books=book_id)
    database.execute(association)
    database.commit()

    return {"message": "Book added to books successfully"}


@app.delete("/author/{author_id}/books/{book_id}/", response_model=None, tags=["Author Relationships"])
async def remove_books_from_author(author_id: int, book_id: int, database: Session = Depends(get_db)):
    """Remove a Book from this Author's books relationship"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship exists
    existing = database.query(books_1).filter(
        (books_1.c.authors == author_id) &
        (books_1.c.books == book_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = books_1.delete().where(
        (books_1.c.authors == author_id) &
        (books_1.c.books == book_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Book removed from books successfully"}


@app.get("/author/{author_id}/books/", response_model=None, tags=["Author Relationships"])
async def get_books_of_author(author_id: int, database: Session = Depends(get_db)):
    """Get all Book entities related to this Author through books"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    book_ids = database.query(books_1.c.books).filter(books_1.c.authors == author_id).all()
    book_list = database.query(Book).filter(Book.id.in_([id[0] for id in book_ids])).all()

    return {
        "author_id": author_id,
        "books_count": len(book_list),
        "books": book_list
    }






############################################
#
#   Library functions
#
############################################

@app.get("/library/", response_model=None, tags=["Library"])
def get_all_library(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Library)
        library_list = query.all()

        # Serialize with relationships included
        result = []
        for library_item in library_list:
            item_dict = library_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            book_list = database.query(Book).join(books, Book.id == books.c.books).filter(books.c.library == library_item.id).all()
            item_dict['books'] = []
            for book_obj in book_list:
                book_dict = book_obj.__dict__.copy()
                book_dict.pop('_sa_instance_state', None)
                item_dict['books'].append(book_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Library).all()


@app.get("/library/count/", response_model=None, tags=["Library"])
def get_count_library(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Library entities"""
    count = database.query(Library).count()
    return {"count": count}


@app.get("/library/paginated/", response_model=None, tags=["Library"])
def get_paginated_library(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Library entities"""
    total = database.query(Library).count()
    library_list = database.query(Library).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": library_list
        }

    result = []
    for library_item in library_list:
        book_ids = database.query(books.c.books).filter(books.c.library == library_item.id).all()
        item_data = {
            "library": library_item,
            "book_ids": [x[0] for x in book_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/library/search/", response_model=None, tags=["Library"])
def search_library(
    database: Session = Depends(get_db)
) -> list:
    """Search Library entities by attributes"""
    query = database.query(Library)


    results = query.all()
    return results


@app.get("/library/{library_id}/", response_model=None, tags=["Library"])
async def get_library(library_id: int, database: Session = Depends(get_db)) -> Library:
    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    book_ids = database.query(books.c.books).filter(books.c.library == db_library.id).all()
    response_data = {
        "library": db_library,
        "book_ids": [x[0] for x in book_ids],
}
    return response_data



@app.post("/library/", response_model=None, tags=["Library"])
async def create_library(library_data: LibraryCreate, database: Session = Depends(get_db)) -> Library:

    if library_data.books:
        for id in library_data.books:
            # Entity already validated before creation
            db_book = database.query(Book).filter(Book.id == id).first()
            if not db_book:
                raise HTTPException(status_code=404, detail=f"Book with ID {id} not found")

    db_library = Library(
        telephone=library_data.telephone,        web_page=library_data.web_page,        address=library_data.address,        name=library_data.name        )

    database.add(db_library)
    database.commit()
    database.refresh(db_library)


    if library_data.books:
        for id in library_data.books:
            # Entity already validated before creation
            db_book = database.query(Book).filter(Book.id == id).first()
            # Create the association
            association = books.insert().values(library=db_library.id, books=db_book.id)
            database.execute(association)
            database.commit()


    book_ids = database.query(books.c.books).filter(books.c.library == db_library.id).all()
    response_data = {
        "library": db_library,
        "book_ids": [x[0] for x in book_ids],
    }
    return response_data


@app.post("/library/bulk/", response_model=None, tags=["Library"])
async def bulk_create_library(items: list[LibraryCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Library entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_library = Library(
                telephone=item_data.telephone,                web_page=item_data.web_page,                address=item_data.address,                name=item_data.name            )
            database.add(db_library)
            database.flush()  # Get ID without committing
            created_items.append(db_library.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Library entities"
    }


@app.delete("/library/bulk/", response_model=None, tags=["Library"])
async def bulk_delete_library(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Library entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_library = database.query(Library).filter(Library.id == item_id).first()
        if db_library:
            database.delete(db_library)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Library entities"
    }

@app.put("/library/{library_id}/", response_model=None, tags=["Library"])
async def update_library(library_id: int, library_data: LibraryCreate, database: Session = Depends(get_db)) -> Library:
    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    setattr(db_library, 'telephone', library_data.telephone)
    setattr(db_library, 'web_page', library_data.web_page)
    setattr(db_library, 'address', library_data.address)
    setattr(db_library, 'name', library_data.name)
    existing_book_ids = [assoc.books for assoc in database.execute(
        books.select().where(books.c.library == db_library.id))]

    books_to_remove = set(existing_book_ids) - set(library_data.books)
    for book_id in books_to_remove:
        association = books.delete().where(
            (books.c.library == db_library.id) & (books.c.books == book_id))
        database.execute(association)

    new_book_ids = set(library_data.books) - set(existing_book_ids)
    for book_id in new_book_ids:
        db_book = database.query(Book).filter(Book.id == book_id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
        association = books.insert().values(books=db_book.id, library=db_library.id)
        database.execute(association)
    database.commit()
    database.refresh(db_library)

    book_ids = database.query(books.c.books).filter(books.c.library == db_library.id).all()
    response_data = {
        "library": db_library,
        "book_ids": [x[0] for x in book_ids],
    }
    return response_data


@app.delete("/library/{library_id}/", response_model=None, tags=["Library"])
async def delete_library(library_id: int, database: Session = Depends(get_db)):
    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    database.delete(db_library)
    database.commit()
    return db_library

@app.post("/library/{library_id}/books/{book_id}/", response_model=None, tags=["Library Relationships"])
async def add_books_to_library(library_id: int, book_id: int, database: Session = Depends(get_db)):
    """Add a Book to this Library's books relationship"""
    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if relationship already exists
    existing = database.query(books).filter(
        (books.c.library == library_id) &
        (books.c.books == book_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = books.insert().values(library=library_id, books=book_id)
    database.execute(association)
    database.commit()

    return {"message": "Book added to books successfully"}


@app.delete("/library/{library_id}/books/{book_id}/", response_model=None, tags=["Library Relationships"])
async def remove_books_from_library(library_id: int, book_id: int, database: Session = Depends(get_db)):
    """Remove a Book from this Library's books relationship"""
    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    # Check if relationship exists
    existing = database.query(books).filter(
        (books.c.library == library_id) &
        (books.c.books == book_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = books.delete().where(
        (books.c.library == library_id) &
        (books.c.books == book_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Book removed from books successfully"}


@app.get("/library/{library_id}/books/", response_model=None, tags=["Library Relationships"])
async def get_books_of_library(library_id: int, database: Session = Depends(get_db)):
    """Get all Book entities related to this Library through books"""
    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    book_ids = database.query(books.c.books).filter(books.c.library == library_id).all()
    book_list = database.query(Book).filter(Book.id.in_([id[0] for id in book_ids])).all()

    return {
        "library_id": library_id,
        "books_count": len(book_list),
        "books": book_list
    }




############################################
#   Library Method Endpoints
############################################




@app.post("/library/{library_id}/methods/cheapest_book_by/", response_model=None, tags=["Library Methods"])
async def execute_library_cheapest_book_by(
    library_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the cheapest_book_by method on a Library instance.

    Parameters:
    - author: Author    """
    # Retrieve the entity from the database
    _library_object = database.query(Library).filter(Library.id == library_id).first()
    if _library_object is None:
        raise HTTPException(status_code=404, detail="Library not found")

    # Prepare method parameters
    author = await get_author(params.get('author'), database)

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_library_object):
            cheapest: Book = None
            price = 1000000000.0
            book_8735197050121 = (await get_books_of_library(_library_object.id, database))['books']
            for i in range(0, len(book_8735197050121)):
                book = book_8735197050121[i]
                if (BAL_contains((await get_authors_of_book(book.id, database))['authors'], author) and (book.price <= price)):
                    cheapest = book
                    price = book.price
            return cheapest.title

        result = await wrapper(_library_object)
        # Commit DB
        database.commit()
        database.refresh(_library_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "library_id": library_id,
            "method": "cheapest_book_by",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Book functions
#
############################################

@app.get("/book/", response_model=None, tags=["Book"])
def get_all_book(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Book)
        book_list = query.all()

        # Serialize with relationships included
        result = []
        for book_item in book_list:
            item_dict = book_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            library_list = database.query(Library).join(books, Library.id == books.c.library).filter(books.c.books == book_item.id).all()
            item_dict['library'] = []
            for library_obj in library_list:
                library_dict = library_obj.__dict__.copy()
                library_dict.pop('_sa_instance_state', None)
                item_dict['library'].append(library_dict)
            author_list = database.query(Author).join(books_1, Author.id == books_1.c.authors).filter(books_1.c.books == book_item.id).all()
            item_dict['authors'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['authors'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Book).all()


@app.get("/book/count/", response_model=None, tags=["Book"])
def get_count_book(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Book entities"""
    count = database.query(Book).count()
    return {"count": count}


@app.get("/book/paginated/", response_model=None, tags=["Book"])
def get_paginated_book(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Book entities"""
    total = database.query(Book).count()
    book_list = database.query(Book).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": book_list
        }

    result = []
    for book_item in book_list:
        library_ids = database.query(books.c.library).filter(books.c.books == book_item.id).all()
        author_ids = database.query(books_1.c.authors).filter(books_1.c.books == book_item.id).all()
        item_data = {
            "book": book_item,
            "library_ids": [x[0] for x in library_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/book/search/", response_model=None, tags=["Book"])
def search_book(
    database: Session = Depends(get_db)
) -> list:
    """Search Book entities by attributes"""
    query = database.query(Book)


    results = query.all()
    return results


@app.get("/book/{book_id}/", response_model=None, tags=["Book"])
async def get_book(book_id: int, database: Session = Depends(get_db)) -> Book:
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    library_ids = database.query(books.c.library).filter(books.c.books == db_book.id).all()
    author_ids = database.query(books_1.c.authors).filter(books_1.c.books == db_book.id).all()
    response_data = {
        "book": db_book,
        "library_ids": [x[0] for x in library_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/book/", response_model=None, tags=["Book"])
async def create_book(book_data: BookCreate, database: Session = Depends(get_db)) -> Book:

    if not book_data.library or len(book_data.library) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Library(s) required")
    if book_data.library:
        for id in book_data.library:
            # Entity already validated before creation
            db_library = database.query(Library).filter(Library.id == id).first()
            if not db_library:
                raise HTTPException(status_code=404, detail=f"Library with ID {id} not found")
    if not book_data.authors or len(book_data.authors) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if book_data.authors:
        for id in book_data.authors:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_book = Book(
        release=book_data.release,        title=book_data.title,        pages=book_data.pages,        genre=book_data.genre.value,        stock=book_data.stock,        price=book_data.price        )

    database.add(db_book)
    database.commit()
    database.refresh(db_book)


    if book_data.library:
        for id in book_data.library:
            # Entity already validated before creation
            db_library = database.query(Library).filter(Library.id == id).first()
            # Create the association
            association = books.insert().values(books=db_book.id, library=db_library.id)
            database.execute(association)
            database.commit()
    if book_data.authors:
        for id in book_data.authors:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = books_1.insert().values(books=db_book.id, authors=db_author.id)
            database.execute(association)
            database.commit()


    library_ids = database.query(books.c.library).filter(books.c.books == db_book.id).all()
    author_ids = database.query(books_1.c.authors).filter(books_1.c.books == db_book.id).all()
    response_data = {
        "book": db_book,
        "library_ids": [x[0] for x in library_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/book/bulk/", response_model=None, tags=["Book"])
async def bulk_create_book(items: list[BookCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Book entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_book = Book(
                release=item_data.release,                title=item_data.title,                pages=item_data.pages,                genre=item_data.genre.value,                stock=item_data.stock,                price=item_data.price            )
            database.add(db_book)
            database.flush()  # Get ID without committing
            created_items.append(db_book.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Book entities"
    }


@app.delete("/book/bulk/", response_model=None, tags=["Book"])
async def bulk_delete_book(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Book entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_book = database.query(Book).filter(Book.id == item_id).first()
        if db_book:
            database.delete(db_book)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Book entities"
    }

@app.put("/book/{book_id}/", response_model=None, tags=["Book"])
async def update_book(book_id: int, book_data: BookCreate, database: Session = Depends(get_db)) -> Book:
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    setattr(db_book, 'release', book_data.release)
    setattr(db_book, 'title', book_data.title)
    setattr(db_book, 'pages', book_data.pages)
    setattr(db_book, 'genre', book_data.genre.value)
    setattr(db_book, 'stock', book_data.stock)
    setattr(db_book, 'price', book_data.price)
    existing_library_ids = [assoc.library for assoc in database.execute(
        books.select().where(books.c.books == db_book.id))]

    librarys_to_remove = set(existing_library_ids) - set(book_data.library)
    for library_id in librarys_to_remove:
        association = books.delete().where(
            (books.c.books == db_book.id) & (books.c.library == library_id))
        database.execute(association)

    new_library_ids = set(book_data.library) - set(existing_library_ids)
    for library_id in new_library_ids:
        db_library = database.query(Library).filter(Library.id == library_id).first()
        if db_library is None:
            raise HTTPException(status_code=404, detail=f"Library with ID {library_id} not found")
        association = books.insert().values(library=db_library.id, books=db_book.id)
        database.execute(association)
    existing_author_ids = [assoc.authors for assoc in database.execute(
        books_1.select().where(books_1.c.books == db_book.id))]

    authors_to_remove = set(existing_author_ids) - set(book_data.authors)
    for author_id in authors_to_remove:
        association = books_1.delete().where(
            (books_1.c.books == db_book.id) & (books_1.c.authors == author_id))
        database.execute(association)

    new_author_ids = set(book_data.authors) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = books_1.insert().values(authors=db_author.id, books=db_book.id)
        database.execute(association)
    database.commit()
    database.refresh(db_book)

    library_ids = database.query(books.c.library).filter(books.c.books == db_book.id).all()
    author_ids = database.query(books_1.c.authors).filter(books_1.c.books == db_book.id).all()
    response_data = {
        "book": db_book,
        "library_ids": [x[0] for x in library_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/book/{book_id}/", response_model=None, tags=["Book"])
async def delete_book(book_id: int, database: Session = Depends(get_db)):
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    database.delete(db_book)
    database.commit()
    return db_book

@app.post("/book/{book_id}/library/{library_id}/", response_model=None, tags=["Book Relationships"])
async def add_library_to_book(book_id: int, library_id: int, database: Session = Depends(get_db)):
    """Add a Library to this Book's library relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_library = database.query(Library).filter(Library.id == library_id).first()
    if db_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    # Check if relationship already exists
    existing = database.query(books).filter(
        (books.c.books == book_id) &
        (books.c.library == library_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = books.insert().values(books=book_id, library=library_id)
    database.execute(association)
    database.commit()

    return {"message": "Library added to library successfully"}


@app.delete("/book/{book_id}/library/{library_id}/", response_model=None, tags=["Book Relationships"])
async def remove_library_from_book(book_id: int, library_id: int, database: Session = Depends(get_db)):
    """Remove a Library from this Book's library relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if relationship exists
    existing = database.query(books).filter(
        (books.c.books == book_id) &
        (books.c.library == library_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = books.delete().where(
        (books.c.books == book_id) &
        (books.c.library == library_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Library removed from library successfully"}


@app.get("/book/{book_id}/library/", response_model=None, tags=["Book Relationships"])
async def get_library_of_book(book_id: int, database: Session = Depends(get_db)):
    """Get all Library entities related to this Book through library"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    library_ids = database.query(books.c.library).filter(books.c.books == book_id).all()
    library_list = database.query(Library).filter(Library.id.in_([id[0] for id in library_ids])).all()

    return {
        "book_id": book_id,
        "library_count": len(library_list),
        "library": library_list
    }

@app.post("/book/{book_id}/authors/{author_id}/", response_model=None, tags=["Book Relationships"])
async def add_authors_to_book(book_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Book's authors relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(books_1).filter(
        (books_1.c.books == book_id) &
        (books_1.c.authors == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = books_1.insert().values(books=book_id, authors=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to authors successfully"}


@app.delete("/book/{book_id}/authors/{author_id}/", response_model=None, tags=["Book Relationships"])
async def remove_authors_from_book(book_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Book's authors relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if relationship exists
    existing = database.query(books_1).filter(
        (books_1.c.books == book_id) &
        (books_1.c.authors == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = books_1.delete().where(
        (books_1.c.books == book_id) &
        (books_1.c.authors == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from authors successfully"}


@app.get("/book/{book_id}/authors/", response_model=None, tags=["Book Relationships"])
async def get_authors_of_book(book_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Book through authors"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    author_ids = database.query(books_1.c.authors).filter(books_1.c.books == book_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "book_id": book_id,
        "authors_count": len(author_list),
        "authors": author_list
    }




############################################
#   Book Method Endpoints
############################################




@app.post("/book/{book_id}/methods/decrease_stock/", response_model=None, tags=["Book Methods"])
async def execute_book_decrease_stock(
    book_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the decrease_stock method on a Book instance.

    Parameters:
    - qty: int    """
    # Retrieve the entity from the database
    _book_object = database.query(Book).filter(Book.id == book_id).first()
    if _book_object is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Prepare method parameters
    qty = params.get('qty')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_book_object):
            """
            Decrease the available stock by the given quantity.

            :param qty: Number of items to remove from stock
            :raises ValueError: If qty is negative or exceeds available stock
            """
            if qty <= 0:
                raise ValueError("Quantity must be a positive integer")

            if qty > _book_object.stock:
                raise ValueError(
                    f"Cannot decrease stock by {qty}. Only {_book_object.stock} items available."
                )

            _book_object.stock -= qty



        result = await wrapper(_book_object)
        # Commit DB
        database.commit()
        database.refresh(_book_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "book_id": book_id,
            "method": "decrease_stock",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



