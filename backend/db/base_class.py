from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

"""
This code is creating a base class for declarative SQLAlchemy models using some advanced techniques:

    * @as_declarative() decorator transforms the Base class into the base for SQLAlchemy declarative models.
    * id field of type Any will become the primary key column in subclasses.
    * name field is an example model field that subclasses can inherit from.
    * @declared_attr decorator defines tablename as a dynamic class attribute rather than instance attribute.
    * tablename method will convert the class name to lowercase to use as the database table name for models.

So models that inherit from this Base class will:

- Automatically get id primary key field
- Inherit the name field on models.
- Get their table name from model class name converted to lowercase.

This allows defining the common table schema and fields in one place - the Base class. 
Models then inherit the common fields and configuration from Base.

The declared_attr and as_declarative decorators help attach the table name logic and base mapping cleanly at the class level.
"""

@as_declarative()
class Base:
    id : Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
