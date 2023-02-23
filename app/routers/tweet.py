from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from app import utils
from app.schemas import TweetResponse, TweetCreate
from app.models import Tweet
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)


@router.get("/", response_model=List[TweetResponse])
def get_tweets(db: Session = Depends(get_db)):
    tweets = db.query(Tweet).all()
    print(tweets)
    return tweets


@router.get("/{id}", response_model=TweetResponse)
def get_tweet(id: int, db: Session = Depends(get_db)):
    tweet = db.query(Tweet).where(Tweet.id==id).first()
    return tweet


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TweetResponse)
def create_tweet(tweet: TweetCreate, db: Session = Depends(get_db)):
    new_tweet = Tweet(**tweet.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return new_tweet


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet(id: int, db: Session = Depends(get_db)):
    tweet_query = db.query(Tweet).where(Tweet.id == id)
    tweet = tweet_query.first()

    if tweet == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id: {id} does not exist"
        )
    
    tweet_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=TweetResponse)
def update_tweet(id: int, updated_tweet: TweetCreate, db: Session = Depends(get_db)):
    tweet_query = db.query(Tweet).where(Tweet.id == id)
    tweet = tweet_query.first()

    if tweet == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet with id: {id} does not exist"
        )
    
    tweet_query.update(
        updated_tweet.dict(),
        synchronize_session=False
    )
    db.commit()
    return tweet_query.first()