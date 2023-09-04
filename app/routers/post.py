from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/api",
    tags=["posts"],
)


@router.get("/posts", response_model=List[schemas.Post])
async def get_all_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


# @router.get("/posts", response_model=List[schemas.Post])
# async def get_all_user_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).filter(
#         models.Post.user_id == current_user.id).all()
#     return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found"
        )
    return post


@router.put("/posts/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized to perform requested action"
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/posts/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized to perform requested action"
        )
    post_query.delete(synchronize_session=False)
    db.commit()

    return {"detail": "Post deleted successfully"}
