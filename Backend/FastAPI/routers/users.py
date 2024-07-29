from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para modelar un objeto

router = APIRouter()

# Inicia el server: uvicorn users:app --reload

# Entidad user
class User(BaseModel): # El BaseModel nos da la capacidad de crear una entidad
    id: int # recomendacion de tiparlo
    name: str 
    surname: str
    url: str
    age: int

users_list = [User(id = 1, name = "Leonardo", surname = "Ulffe", url = "https://google.com", age = 21),
         User(id = 2, name = "Josue", surname = "Torres", url = "https://x.com", age = 30),
         User(id = 3, name = "Leo", surname = "Uribe", url = "https://facebook.com", age = 19)]

# Url local: http://127.0.0.1:8000
@router.get("/usersjson") # esta es la raiz donde se despliega
async def usersjson():
    return [{"name": "Leonardo", "surname": "Ulffe", "url": "https://google.com", "age": 21},
            {"name": "Josue", "surname": "Torres", "url": "https://x.com", "age": 30},
            {"name": "Leo", "surname": "Uribe", "url": "https://facebook.com", "age": 19}]

@router.get("/users") # esta es la raiz donde se despliega
async def users():
    return users_list

# Path
@router.get("/user/{id}") # esta es la raiz donde se despliega
async def user(id: int):
    return search_user(id)

# Query 
@router.get("/user/") # Parametro de Query
async def user(id: int):
    return search_user(id)
    
@router.post("/user/", response_model=User, status_code=201) 
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail = "El usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/user/") 
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user
    
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
        
    if not found:
        return {"error": "No se ha encontrado el usuario"}



def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado un usuario"}

