from fastapi import APIRouter, HTTPException
from crud.user import user_crud
from schemas import user as user_schema

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/",response_model=user_schema.User)
def create_user_endpoint(user: user_schema.UserCreate):
    return user_crud.create_user(user)


@user_router.get("/{user_id}",response_model=user_schema.User)
def get_user_by_id(user_id: str):
    user = user_crud.get_user(user_id)
    if user:
        return user
    raise HTTPException(404, detail="Todo does not exit")



@user_router.get("/",response_model=list[user_schema.User])
def list_users():
    users = user_crud.list_users()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@user_router.put("/{user_id}", response_model=user_schema.User)
def update_user_endpooint(user_id: str, update_user: user_schema.UserUpdate):
    updated_user = user_crud.update_user(user_id, update_user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@user_router.delete("/{user_id}")
def delete_user(user_id: str):
    if not user_crud.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}



