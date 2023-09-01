from sqlalchemy.orm import Session
from schemas.blog import BlogCreate, UpdateBlog
from db.models.blog import Blog

'''
Session methods

  add(model):         Adds a new model instance to be persisted to the database.
  delete(model):      Deletes the specified model instance from the database.
  query(Model):       Starts building a query against the given model class.
  commit():           Commits any pending changes to the database.
  rollback():         Rolls back any pending changes and returns the session to a clean state.
  flush():            Synchronizes pending changes to the database but doesn't commit yet.
  expire(model):      Expires the session's cached copy of the given model instance.
  refresh(model):     Refreshes the session's state from the database for the given instance.
  close():            Closes the session. Should be called when done with a session.
  execute(statement): Executes a raw SQL statement.
  scalars(statement): Executes a statement and returns scalar results.
  connection():       Returns the underlying database connection.
'''

def create_new_blog(blog: BlogCreate, db: Session, author_id: int = 1):
    blog = Blog(
                title = blog.title,
                slug = blog.slug,
                content = blog.content,
                author_id = author_id
                )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id==id).first()
    return blog

def retrieve_all_active_blogs(db: Session):
    blogs = db.query(Blog).filter(Blog.is_active==True).all()
    return blogs

def update_blog_by_id(id: int, blog: UpdateBlog, db: Session, author_id: int):
    blog_in_db = db.query(Blog).filter(Blog.id==id).first()
    if not blog_in_db:
        return {"error": f"Blog with {id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error": f"Only the author can modify the blog"}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content

    db.add(blog_in_db)
    db.commit()
    return blog_in_db

# requires also author_id to validate that a correct blog will  be deleted
def delete_blog_by_id(id: int, db: Session, author_id: int):
    blog_in_db = db.query(Blog).filter(Blog.id==id).first()
    if not blog_in_db:
        return {"error":f"Could not find blog with the id {id}"}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only an author can delete a blog"}
    if blog_in_db.author_id != author_id:
        return {"error": "Not authorized to delete this blog"}
    
    # blog_in_db.delete() will reach the same effect 
    # both "db" and "blog_in_db" are instance of Session
    db.commit()
    db.delete(blog_in_db) 
    return {"msg":f"Deleted blog with id {id}"}