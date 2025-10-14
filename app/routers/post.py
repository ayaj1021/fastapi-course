from typing import List, Optional
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from fastapi import Response, status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/posts",
    # This tag is to separate our endpoints in our doc into different sections
    tags=["Posts"],
)




# @router.get("/", response_model=List[schema.PostResponse])
@router.get("/", response_model=List[schema.PostOut])
async def get_post(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    # limit here is a query param that works with limiting the number of posts we send
    # Just like for pagination
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # all_posts = my_posts
    # This is to get the data from our database
    # cursor.execute("""SELECT * FROM posts""")
    # this cursor.fetchall is to fetch all the posts for us
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).all()
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    # THis is to add the votes count to our response
    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.ilike(f"%{search}%"))
        .limit(limit)
        .offset(skip)
        .all()
    )

    formatted_results = [{"Post": post, "votes": votes} for post, votes in posts]

    # return {"data": posts}
    #  return posts
    return formatted_results


@router.get("/user{id}", response_model=List[schema.PostResponse])
async def get_user_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # all_posts = my_posts
    # This is to get the data from our database
    # cursor.execute("""SELECT * FROM posts""")
    # this cursor.fetchall is to fetch all the posts for us
    # posts = cursor.fetchall()
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    posts = db.query(models.Post).filter(models.Post.user_id == id).all()
    # return {"data": posts}
    return posts


@router.get("/{id}", response_model=schema.PostOut)
async def get_single_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # print(new_get_post)
    # post = find_post(id)
    post = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    # return {"data": post}

    post_data, votes = post

    formatted_results = {"Post": post_data, "votes": votes} 
    return formatted_results


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse
)
async def create_post(
    post_data: schema.PostCreate,
    db: Session = Depends(get_db),
    # This is to check if the user is logged in before they can create a post
    current_user: int = Depends(oauth2.get_current_user),
):
    # This was what we had when we hardcoded our list in memory
    # post_dict = post_data.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.routerend(post_dict)

    # This section is to now create to our database
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post_data.title, post_data.content, post_data.published),
    # )

    # new_post = cursor.fetchone()
    # # We need to actually do this to actually save our data into our database
    # conn.commit()
    # To avoid manually typing out our request body to create a post, what we can do is actually
    # use .model_dump() then we also unpack it

    # **post_data.model_dump()
    # new_post =models.Post(
    #     title=post_data.title, content=post_data.content, published=post_data.published
    # )

    new_post = models.Post(user_id=current_user.id, **post_data.model_dump())
    # create a new post
    db.add(new_post)
    # commit the post
    db.commit()
    # Get back the post
    db.refresh(new_post)
    # return {"data": new_post}
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # # index = find_index_post(id)
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post.user_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )
    # my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
async def update_post(
    id: int,
    post_data: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts  SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, (str(id))),
    # )

    # new_updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    # return {"data": post_query.first()}
    return post_query.first()
