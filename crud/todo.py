from serializers import todo as serializer
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.todo import TodoCreate, TodoUpdate
from database import todo_collection


class TodoCrud:

    @staticmethod
    def create_todo(todo_data: TodoCreate):
        todo_data = jsonable_encoder(todo_data)  # So this jsonable_encoder will convert this todo_data to json object so that our mongodb can understand
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)


    @staticmethod
    def get_todo(todo_id: str):
        todo_valid = ObjectId.is_valid(todo_id)
        if not todo_valid:
            return None 
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            return serializer.todo_serializer(todo) 
        return None
     
    @staticmethod
    def list_todos():
        todos_find = todo_collection.find() 
        todos_list = list(todos_find)  
        
        if not todos_list:
            return None 
        
        return serializer.todos_serializer(todos_list)  


    @staticmethod
    def update_todo(todo_id: str, todo_update: TodoUpdate):
        if not ObjectId.is_valid(todo_id):
            return None  

        updated_todo =  todo_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": jsonable_encoder(todo_update)},
            return_document=True 
        )

        if updated_todo:
             return serializer.todo_serializer(updated_todo)
        
        return None



    @staticmethod
    def delete_todo(todo_id: str):
        if not ObjectId.is_valid(todo_id):
            return None 
        deleted_todo =  todo_collection.delete_one({"_id": ObjectId(todo_id)})

        if deleted_todo:
            return serializer.todo_serializer(deleted_todo)
        else:  None


    @staticmethod
    def list_todos_by_user(user_id: str):
        todos =  list(todo_collection.find({"user_id":  user_id}).to_list(None))
        return [serializer.todo_serializer(todo) for todo in todos]
       

todo_crud = TodoCrud()