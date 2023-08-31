from typing import Optional, List
from pydantic import BaseModel, root_validator
from datetime import datetime
"""
Pydantic schema classes define the structure and validation 
requirements for request and response data.

These schema classes can be used as response models to define 
the shape of response returned from a path operation.

However, response models are not necessarily tied to router functions only. They can be used for:

  *  Path operation response models
  *  WebSocket response models
  *  Dependency response models
  *  Parameter convertors

  The router functions themselves usually return the data directly rather than models.

  FastAPI will serialize the router function return data to match the declared response model automatically.
"""
class BlogCreate(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    '''
    The root_validator decorator is used to define a validation function called 
    generate_slug that runs before the model's validation. It generates the slug 
    value based on the title value by replacing spaces with hyphens and converting 
    to lowercase. This ensures that the slug is automatically generated 
    from the provided title if it exists.
    '''
    @root_validator(pre=True)
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values
    
'''
The Config inner class with the attribute from_attributes = True is used to indicate 
that this model should be created from attributes. This means that when you create 
an instance of ShowBlog, you can pass in the attributes directly, and they will 
be validated and structured according to the model's definition.
'''

"""
Schema classes are used as response_model and response model is something that router function returns
"""
class ShowBlog(BaseModel):
    title: str
    content: Optional[str]
    author_id: int
    created_at: datetime

    class Config():
        from_attributes = True

# Schema is the same as for creating blog 
class UpdateBlog(BlogCreate):
    pass