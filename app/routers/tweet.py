from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from app import utils
from app.schemas import TweetResponse, TweetCreate, TweetOut
from app.models import Tweet, Like
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from typing import List
from .. import oauth2

router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)


@router.get("/", response_model=List[TweetOut])
def get_tweets(db: Session = Depends(get_db)):
    print('hello')
    tweets = db.query(Tweet, func.count(Like.tweet_id).label("likes")).join(Like, Like.tweet_id == Tweet.id, isouter=True).group_by(Tweet.id).all()
    return tweets


@router.get("/{id}", response_model=TweetOut)
def get_tweet(id: int, db: Session = Depends(get_db)):
    tweet = db.query(Tweet, func.count(Like.tweet_id).label("likes")).join(Like, Like.tweet_id == Tweet.id, isouter=True).group_by(Tweet.id).where(Tweet.id == id).first()
    return tweet


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TweetResponse)
def create_tweet(tweet: TweetCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user)
    new_tweet = Tweet(owner_id=current_user.id, **tweet.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tweet_query = db.query(Tweet).where(Tweet.id == id)
    tweet = tweet_query.first()

    if tweet == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id: {id} does not exist"
        )
    
    if tweet.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"tweet with id: {id} does not belong to the current user"
        )
    
    tweet_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=TweetResponse)
def update_tweet(id: int, updated_tweet: TweetCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tweet_query = db.query(Tweet).where(Tweet.id == id)
    tweet = tweet_query.first()

    if tweet == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet with id: {id} does not exist"
        )
    
    if tweet.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"tweet with id: {id} does not belong to the current user"
        )
    
    tweet_query.update(
        updated_tweet.dict(),
        synchronize_session=False
    )
    db.commit()
    return tweet_query.first()