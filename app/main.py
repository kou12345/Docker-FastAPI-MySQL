from fastapi import FastAPI

from routers import task, done  # type: ignore

app = FastAPI()

app.include_router(task.router)
app.include_router(done.router)


@app.get("/")
def get_root():
    return {"Hello": "FastAPI"}
