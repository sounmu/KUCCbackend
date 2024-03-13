from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def read_name(name: str):
    return {"message": f"Hello, {name}!"}
