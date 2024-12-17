from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=List[schemas.PostOut])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts_query = db.query(models.Post)
    posts = posts_query.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts_with_votes = []
    # posts_with_votes: List[schemas.PostOut] = []
    # for post, votes in results:
    #     post_data = schemas.PostOut(
    #             id=post.id,
    #             title=post.title,
    #             content=post.content,
    #             published=post.published,
    #             created_at=post.created_at,
    #             user_id=post.user_id,
    #             user=post.user,
    #             votes=votes
    #             )
    #     posts_with_votes.append(post_data)
    # print(posts_with_votes)
    for post, votes in results:
        post_data = {
                "Post": 
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "published": post.published,
                    "user_id": post.user_id, 
                    "user":
                        {
                            "id": post.user.id, 
                            "email": post.user.email, 
                            "created_at": post.user.created_at
                        }
                },
                "votes": votes,
            }
        posts_with_votes.append(post_data)

    return posts_with_votes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# @router.get("/{id}", response_model=schemas.PostOut)
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found")
    
    # if result.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    posts_with_votes = []
    post_data = {
            "Post": 
            {
                "id": post[0].id,
                "title": post[0].title,
                "content": post[0].content,
                "published": post[0].published,
                "user_id": post[0].user_id, 
                "user":
                    {
                        "id": post[0].user.id, 
                        "email": post[0].user.email, 
                        "created_at": post[0].user.created_at
                    }
            },
            "votes": post[1],
        }
    posts_with_votes.append(post_data)

    return posts_with_votes

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return {Response(status_code=status.HTTP_204_NO_CONTENT)}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post