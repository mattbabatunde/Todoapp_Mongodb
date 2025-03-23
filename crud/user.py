from serializers import user as serializer
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.user import UserCreate, UserUpdate
from database import user_collection


class UserCrud:

    @staticmethod
    def create_user(user_data: UserCreate):
        user_data = jsonable_encoder(user_data)
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)
    

    @staticmethod
    def get_user( user_id: str):
        is_user_valid = ObjectId.is_valid(user_id)
        if not is_user_valid:
            return None
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return serializer.user_serializer(user)
        return None
    
        
        

    @staticmethod
    def list_users():
        users_find = user_collection.find()
        user_list = list(users_find)
        if not user_list:
            return None
        return serializer.users_serializer(user_list)
    

    @staticmethod
    def update_user(user_id: str, user_update: UserUpdate):
        if not ObjectId.is_valid(user_id):
            return None
        
        updated_user = user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": jsonable_encoder(user_update)},
            return_document=True
        )

        if updated_user:
            return serializer.user_serializer(updated_user)
        
        return None

    

    @staticmethod
    def delete_user( user_id: str):
       if not ObjectId.is_valid(user_id):
           return None
       deleted_user = user_collection.find_one_and_delete({"_id": ObjectId(user_id)})
       if deleted_user:
          return serializer.user_serializer(deleted_user)
       return None



user_crud = UserCrud()


