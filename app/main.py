from fastapi import FastAPI
from .routers import tweet, user, auth, like
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tweet.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

@app.get('/')
def root():
    return {"Message": "Base Project"}
