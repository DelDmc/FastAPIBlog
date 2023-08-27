from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from typing import Generator


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SESSIONLOCAL = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SESSIONLOCAL()
        yield db
    finally:
        db.close()



'''
The get_db() function is a utility function designed to manage SQLAlchemy sessions in a 
FastAPI application (or similar frameworks). 

SQLALCHEMY_DATABASE_URL: 
This constant holds the database connection URL, 
which is read from the application's settings. 
It's typically in the format: "postgresql://user:password@host:port/database".

engine: 
The create_engine() function creates a SQLAlchemy database engine using the provided database URL. 
The engine represents a connection pool to the database and handles connections for you.

SESSIONLOCAL: 
This is an instance of sessionmaker, which is a factory for creating new SQLAlchemy sessions. 
It's configured to create sessions associated with the engine you've defined. The options autoflush=False and 
autocommit=False are used to specify that the session should not automatically 
flush changes to the database or automatically commit transactions.

get_db() function: 
This function is a generator function, indicated by the yield keyword. 
The try block starts by creating a session using the SESSIONLOCAL() factory. The yield db statement temporarily 
pauses the function's execution and provides the session (db) to the caller. This is important for dependency injection in FastAPI.

When the caller is done using the session, the finally block ensures that the session is properly 
closed using the db.close() call. Closing the session releases the connection back to the connection pool.

This pattern of using a generator function (yielding resources) and ensuring resource cleanup (finally block) is 
common in FastAPI and other frameworks to handle context-dependent resources like database sessions.

In summary, the get_db() function is a utility to manage SQLAlchemy sessions, creating a session when needed, 
providing it to the caller, and ensuring it's properly closed afterward. This helps manage database connections and
transactions in a clean and efficient way, especially in asynchronous web frameworks like FastAPI.
'''