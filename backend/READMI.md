### Project Files Structure

```
FastAPICourse
├── backend
│   ├── alembic
│   │   └── versions
│   ├── apis
│   │   └── v1
│   │       ├── route_blog.py
│   │       ├── route_login.py
│   │       └── route_user.py
│   ├── core
│   │   ├── config.py
│   │   ├── hashing.py
│   │   └── security.py
│   ├── db
│   │   ├── models
│   │   │   ├── blog.py
│   │   │   └── user.py
│   │   ├── repository
│   │   │   ├── blog.py
│   │   │   ├── login.py
│   │   │   └── user.py
│   │   ├── base.py
│   │   └── session.py
│   ├── schemas
│   │   ├── blog.py
│   │   └── user.py
│   ├── tests
│   │   ├── conftest.py
│   │   └── test_routes
│   │       └── test_user.py
│   ├── .env
│   ├── alembic.ini
│   ├── main.py 
│   └── README.md
├── venv
├── .gitignore
└── requirements.txt
```


### Typical request flow in FastAPI:

The request is received by FastAPI and directed to the appropriate router based on the path and method.

Before reaching the router function, the request goes through the validation middleware:

 - Pydantic schemas validate the request body, query params, etc.
 - Header, cookie, security schemes are also validated.
 - After validation, any dependencies declared in the router function are resolved. This includes:
    * Database sessions
    * Authentication and security checks
    * Extracting elements from request for use in function

The router function is executed with the validated and deserialized parameters.

The router function returns the response content directly or uses **response models**.

On the way out, **response models** validate and serialize the response.

Any other middleware can process the response.

The response is sent back to the client.

So in summary:

- Request -> Router matching -> Validation and deserialization
- Execute router function -> Create response
- Serialization and validation -> Additional middleware -> Send response

The key points are that validation and serialization happen automatically before and after the router function rather than within it.

### Uvicorn

Uvicorn is a high-performance ASGI server to run asynchronous Python apps in production and development. 
It provides the core server implementation that frameworks like FastAPI build upon.
Here are some key points on Uvicorn and how to use it:

- Implements the ASGI specification for running asynchronous Python web apps and frameworks.
- Built on top of uvloop and httptools for fast HTTP handling.
- Supports HTTP protocols like HTTP/1.1 and WebSockets.
- Can be used to serve ASGI frameworks like FastAPI, Starlette, Django Channels. 
- Provides configuration options like host, port, reload, log level etc.
- Integrates with gunicorn for production deployments.

To use Uvicorn:

- Install with `pip install uvicorn`

- Run like: 

```
uvicorn main:app --reload
```

- main:app points to the app object instance to serve
- --reload enables auto restart on code changes
- Provide additional configuration flags as needed


### Alembic

**Alembic** is a database migration tool used for managing schema changes in SQLAlchemy database projects. Some key points about Alembic:

  * It generates migration scripts to incrementally update the database schema.
  * Migrations include logic to upgrade to a new schema version and downgrade backwards.
  * Alembic tracks which migrations have been applied to the database already.
  * New migrations can be generated automatically based on model changes.
  * It supports environments like development, testing, production for applying migrations.
  * Migration scripts are Python code containing SQLAlchemy commands.
  * Enables safely evolving the database schema over time in a versioned manner.

In summary, Alembic handles:

  * Migration generation based on model changes
  * Tracking migration history
  * Applying and rolling back migrations
  * Environments and branching
  * It gives fine-grained control over evolving the database schema and provides integration with SQLAlchemy models and environment management. 
  * Overall, a very useful tool for database change management in Python projects.


### Pydantic

Pydantic is a Python library for data validation and settings management using Python type hints. 
Here is an overview and some examples:

- It uses type hints to validate data and enforce structure. For example:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    signup_ts: datetime

user = User(id=123, name='John', signup_ts='2022-01-01T00:00:00') 
# Validates the data
```

- Pydantic models can validate dict, JSON, environment variables and more.
- Provides validation errors with useful messages.
- Can define nested models, custom validations, config defaults etc.

```python
from pydantic import BaseModel, validator

class Payment(BaseModel):
    amount: float
    currency: str
    
    @validator('amount')
    def amount_must_be_positive(v):
        if v <= 0:
            raise ValueError('Amount must be positive')
```

- Integrates with other parts of the Python ecosystem like ORM libraries.
- Used extensively in FastAPI for request and response validation.

Pydantic brings the benefits of type checking for validation and settings management in Python. 
An essential tool for robust and maintainable applications.




