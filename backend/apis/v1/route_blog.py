from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.user import User
from apis.v1.route_login import get_current_user
from schemas.blog import BlogCreate, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, retrieve_all_active_blogs, update_blog_by_id, delete_blog_by_id

router = APIRouter()

@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    blog = create_new_blog(blog=blog, db=db, author_id=1)
    return blog


@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: int, db:Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog with {id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return blog

@router.get("", response_model=List[ShowBlog])
def get_all_active_blogs(db:Session = Depends(get_db)):
    blogs = retrieve_all_active_blogs(db=db)
    if not blogs:
        raise HTTPException(detail=f"No active blogs in repository yet", status_code=status.HTTP_404_NOT_FOUND)
    return blogs

@router.put("/{id}", response_model=ShowBlog)
def update_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    blog = update_blog_by_id(id=id, blog=blog, db=db, author_id=current_user.id)
    if isinstance(blog, dict):
        raise HTTPException(
            detail=blog.get("error"),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return blog

@router.delete("/{id}")
def delete_blog(id: int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message = delete_blog_by_id(id=id, db=db, author_id=current_user.id)
    if message.get("error"):
        raise HTTPException(detail=message.get("error"), status_code=status.HTTP_404_NOT_FOUND)
    return {"msg":message.get("msg")}
