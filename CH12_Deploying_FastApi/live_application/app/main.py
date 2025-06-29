from fastapi import FastAPI

app = FastAPI(title="Fast APi Live Application")


@app.get("/")
def read_root():
    return {"hello": "world"}