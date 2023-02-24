from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, oauth2
from ..schemas import LikeCreated
from ..models import Like, Tweet

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: LikeCreated, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    tweet = db.query(Tweet).where(Tweet.id == like.tweet_id).first()
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id: {like.tweet_id} does not exist"
        )

    like_query = db.query(Like).filter(Like.tweet_id == like.tweet_id, Like.user_id == current_user.id)
    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on tweet {like.tweet_id}"
            )
        
        new_like = Like(tweet_id=like.tweet_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"Message": "Successfully added vote"}
    else: 
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Like does not exist"
            )
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Successfully deleted vote"}
