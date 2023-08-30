from typing import Optional, List
from pydantic import BaseModel, root_validator
from datetime import datetime

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
class ShowBlog(BaseModel):
    title: str
    content: Optional[str]
    created_at: datetime

    class Config():
        from_attributes = True

class ShowAllBlogs(BaseModel):
    blogs: List[ShowBlog]
    total: int

    class Config():
        from_attributes = True