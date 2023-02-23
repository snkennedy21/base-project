from fastapi import FastAPI, status, HTTPException, Response, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .models import Base, Tweet

models.Base.metadata.create_all(bind=engine)

class TweetIn(BaseModel):
    content: str

app = FastAPI()


# Attempt to connec to database every 5 seconds
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database='twitter-clone',
            user="postgres",
            password='rockband',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database Connection Success")
        break
    except Exception as error:
        print("Database Connection Failure")
        print("Error: ", error)
        time.sleep(5)


@app.get('/')
def root():
    return {"Message": "Hello World"}



@app.get("/tweets")
def get_tweets(db: Session = Depends(get_db)):
    tweets = db.query(Tweet).all()
    return {"tweets": tweets}


@app.get("/tweets/{id}")
def get_tweet(id: int, db: Session = Depends(get_db)):
    tweet = db.query(Tweet).where(Tweet.id==id).first()
    return {"tweet": tweet}


@app.post("/tweets", status_code=status.HTTP_201_CREATED)
def create_tweet(tweet: TweetIn, db: Session = Depends(get_db)):
    new_tweet = Tweet(**tweet.dict())
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return {"data": new_tweet}


@app.delete("/tweets/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/tweets/{id}")
def update_tweet(id: int, updated_tweet: TweetIn, db: Session = Depends(get_db)):
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