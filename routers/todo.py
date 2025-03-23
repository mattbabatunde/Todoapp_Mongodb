from fastapi import APIRouter, HTTPException
from crud.todo import todo_crud
from schemas import todo as todo_schema


router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=todo_schema.Todo)
def create_todo_endpoint(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)





@router.get("/{todo_id}", response_model=todo_schema.Todo)
def get_todo_endpoint(todo_id: str):
    todo =  todo_crud.get_todo(todo_id)
    if todo:
        return todo
    raise HTTPException(404, detail="Todo does not exit")


@router.get("/", response_model=list[todo_schema.Todo])
def list_todos_endpoint():
    todos = todo_crud.list_todos()
    if todos:
        return todos
    
    raise HTTPException(404, detail="No todos found")


@router.put("/{todo_id}", response_model=todo_schema.Todo)
def update_todo_endpoint(
    todo_id: str, todoupdate: todo_schema.TodoUpdate
):
    updated_todo = todo_crud.update_todo(todo_id, todoupdate)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: str):
    if not todo_crud.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@router.get("/{user_id}", response_model=list[todo_schema.Todo])
def get_todos_for_user(user_id: str):
    todos = todo_crud.list_todos_by_user(user_id)
    if not todos:
        raise HTTPException(status_code=404, detail="No todos found for this user")
    return todos