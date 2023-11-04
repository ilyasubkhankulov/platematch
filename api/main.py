from fastapi import FastAPI

app = FastAPI()

app.get("/")(lambda: {"Hello": "World"})
