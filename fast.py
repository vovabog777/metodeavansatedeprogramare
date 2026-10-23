from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("items/index.html")


@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI! 👋"}