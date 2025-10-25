from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, votes


# import PostCreate, PostResponse

#Because we are using  alembic we don't really need this
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()


#This is to allow other domains talk to our api.
#This under we will specify the domains we want to talk to our API
# origins = ["https://www.google.com"]

#If we want to domains to talk to our APIs do 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is to reference all of our routes that we have in different files
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)



# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i





@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.get("/sqlalchemy")
# async def test_posts(db: Session = Depends(get_db)):
#     # This is to query all the data we have in our database i.e to get all the data using sqlalchemy
#     # Instead of we using raw sql
#     posts = db.query(models.Post).all()
#     return {"data": posts}
