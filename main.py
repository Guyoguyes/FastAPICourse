from typing import Optional

from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    # Default value
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]


@app.get('/')
def root():
    return {'data': my_posts}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}


# title string, content string
@app.post('/posts')
def create_post(newPost: Post):
    print(newPost)
    print(newPost.dict())
    post_dict = newPost.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return {"data": p}
        # else:
        #     return {"data": f"No post of id {id} is Found"}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    found_post = find_post(id)
    if not found_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"No post of {id} is found"}
    return {"data": found_post}
