from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
from typing import Annotated


# This is our schema
# This is pydantic model
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# Instead of having different classes for create and update post, we can actually use one class
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# We using OOP where this will inherit it's data from the post base class
# pass means we are not changing anything from it
class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True 


#This is a class for the response
class PostResponse(PostBase):
    # status: bool
#Instead of we repeating ourselves for the title content and published we just extend the 
#post base model and remove the repeated fields
    # title: str
    # content: str
    # published: bool
    id: int
    user_id: int
    created_at: datetime
    #We add the owner to our schema here to get it as part of our response
    owner: UserResponse
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
            orm_mode = True

     



class CreateUser(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1, ge=0)]
    


#We need to make our users password secure by making converting to hash
#So we install passlib  pip install passlib[bcrypt] Though already installed here
#So there was an issue with the bcrypt because it said we need a hard limit of 72 characters
#So we are going to use pip install passlib[argon2]