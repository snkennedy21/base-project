from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import tweet, user, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(tweet.router)
app.include_router(user.router)
app.include_router(auth.router)


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
