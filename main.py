from fastapi import FastAPI
from routers import  user, todo




app = FastAPI()


app.include_router(user.user_router)
app.include_router(todo.todo_router)


@app.get("/")
def home():
    return {"message": "Hello"}