from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    # Default value
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='loalhost', database='', user='', password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful")
        break
    except Exception as error:
        print(f"Database connection error: {error}")


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]


@app.get('/')
def root():
    return {'data': my_posts}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}


# title string, content string
@app.post('/posts', status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"No post of {id} is found"}
    return {"data": found_post}


def find_post_bt_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    posts = find_post_bt_index(id)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post of id {id} is not found')
    my_posts.pop(posts)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    posts = find_post_bt_index(id)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post of id {id} is not found')
    posts_dic = post.dict()
    posts_dic['id'] = id
    my_posts[posts] = posts_dic
    return {"data": posts_dic}