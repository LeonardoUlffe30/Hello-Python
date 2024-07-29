from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


app.mount("/static", StaticFiles(directory = "static"), name = "static")

# @: decorador de operaciones de path
# Métodos o operaciones de HTTP: GET, POST, PUT, DELETE
# async: para realizar la operacion en segundo plano al llamar a un servidor

# Url local: http://127.0.0.1:8000
@app.get("/") # esta es la raiz donde se despliega
async def root():
    return "¡Hola FastAPI!"

# Url local: http://127.0.0.1:8000/url
@app.get("/url") # esta es la raiz donde se despliega
async def url():
    return { "url_curso":"https://mouredev.com/python" }


# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc