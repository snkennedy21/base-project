from fastapi import FastAPI, status, HTTPException, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel


class Tweet(BaseModel):
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
def get_tweets():
    cursor.execute(
        '''
        SELECT * FROM tweets
        '''
    )
    tweets = cursor.fetchall()
    print(tweets)
    return {"tweets": tweets}


@app.get("/tweets/{id}")
def get_tweet(id: int):
    cursor.execute(
        '''
        SELECT * 
        FROM tweets
        WHERE id = %s
        ''',
        (str(id),)
    )
    tweet = cursor.fetchone()
    return {"tweet": tweet}


@app.post("/tweets", status_code=status.HTTP_201_CREATED)
def create_tweet(tweet: Tweet):
    print(tweet)
    cursor.execute(
        '''
        INSERT INTO tweets
        (content)
        VALUES (%s)
        RETURNING *
        ''',
        (tweet.content,)
    )
    new_tweet = cursor.fetchone()
    conn.commit()
    return {"data": new_tweet}


@app.delete("/tweets/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tweet(id: int):
    cursor.execute(
        '''
        DELETE FROM tweets
        WHERE id = %s
        RETURNING *
        ''',
        (str(id),)
    )
    deleted_tweet = cursor.fetchone()
    conn.commit()
    if deleted_tweet == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id: {id} does not exist"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/tweets/{id}")
def update_tweet(id: int, tweet: Tweet):
    cursor.execute(
        '''
        UPDATE tweets
        SET content = %s
        WHERE id = %s
        RETURNING *
        ''',
        (tweet.content, str(id))
    )
    updated_tweet = cursor.fetchone()
    conn.commit()
    if updated_tweet == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with id: {id} does not exist"
        )
    
    return {"data": updated_tweet}