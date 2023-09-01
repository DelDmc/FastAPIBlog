from fastapi import APIRouter
from apis.v1 import route_user
from apis.v1 import route_blog
from apis.v1 import route_login

"""
api_router = APIRouter() creates the main router
api_router.include_router() is used to include each individual router under the main api_router
The prefix argument sets the path prefix for all routes in that router
The tags argument is used to tag all the routes from a router with a tag name
The tags are useful for:

  * Grouping related routes together in documentation
  * Filtering routes by tag for testing etc
  * Adding metadata like descriptions to tags

The tags help organize and categorize related routes together for documentation and testing purposes. 
You can also filter routes by tag, e.g. app.routes(tags=["users"]) gets only user routes. 
"""


api_router = APIRouter()

api_router.include_router(route_user.router, prefix='/users', tags=["Users"])
api_router.include_router(route_blog.router, prefix='/blogs', tags=["Blogs"])
api_router.include_router(route_login.router, prefix='', tags=["Login"])
