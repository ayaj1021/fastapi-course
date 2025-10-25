from app import schema
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schema.PostOut(**post)

    # posts = schema.PostOut(res.json())

    # def validate(post):
    #     return PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(posts_list)

    assert len(res.json()) == len(test_posts)

    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_found(authorized_client, test_posts):
    res = authorized_client.get("/posts/9999")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schema.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("New Title 1", "New Content 1", True),
        ("New Title 2", "New Content 2", False),
        ("New Title 3", "New Content 3", True),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published},
    )
    created_post = schema.PostResponse(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]
    assert res.status_code == 201


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/",
        json={"title": "New Title", "content": "New Content"},
    )
    created_post = schema.PostResponse(**res.json())
    assert created_post.title == "New Title"
    assert created_post.content == "New Content"
    assert created_post.published is True
    assert created_post.user_id == test_user["id"]
    assert res.status_code == 201


def test_unauthorized_user_create_posts(client, test_user, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "New Title", "content": "New Content"},
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    post_to_delete = test_posts[0]
    res = authorized_client.delete(f"/posts/{post_to_delete.id}")
    assert res.status_code == 204


def test_delete_post_not_found(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/9999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    post_to_delete = test_posts[3]  # Assuming this post belongs to another user
    res = authorized_client.delete(f"/posts/{post_to_delete.id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    post_to_update = test_posts[0]
    res = authorized_client.put(
        f"/posts/{post_to_update.id}",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": False,
        },
    )
    updated_post = schema.PostResponse(**res.json())
    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Updated Content"
    assert updated_post.published is False
    assert res.status_code == 200


# def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):

#     post_to_update = test_posts[3]
#     data = (
#         {
#             "title": "updated title",
#             "content": "updated content",
#             "id": post_to_update.id,
#         },
#     )
#     res = authorized_client.put(
#         f"/posts/{post_to_update.id}",
#         json=data,
#     )

#     updated_post = schema.PostResponse(**res.json())
#     assert updated_post.title == data["title"]
#     assert updated_post.content == data["content"]
#     assert updated_post.published is False
#     assert res.status_code == 403
