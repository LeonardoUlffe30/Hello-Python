from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# OAuth2PasswordBearer = se encarga de gestionar el usuario y contraseña de autenticacion
# OAuth2PasswordRequestForm = forma en la que se va a enviar a nuestro backend estos criterios de autenticacion

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

class User(BaseModel): 
    username: str 
    full_name: str
    email: str 
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "leonardo": {
        "username": "leoulffe",
        "full_name": "Leonardo Ulffe",
        "email": "leonardo.ulffe.2003@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "leonardo2": {
        "username": "leoulffe2",
        "full_name": "Leonardo Ulffe2",
        "email": "leonardo.ulffe.2003@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=401, detail = "Credenciales de autenticacion inválidas", 
                            headers = {"WWW-Authenticate":"Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=400, detail = "Usuario inactivo")
    
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not users_db:
        raise HTTPException(status_code=400, detail = "El usuario no es correcto")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail = "La contraseña no es correcta")

    return {"access_token" : user.username, "token_type" : "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user