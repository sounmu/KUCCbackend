from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


class Memo(BaseModel):
    id: Optional[int] = None
    title: str
    content: str


memos = []


app = FastAPI()


@app.post("/memos/")
def create_memo(memo: Memo):
    memo.id = len(memos) + 1
    memos.append(memo.dict())
    return memo


@app.get("/memos/")
def read_memos():
    return memos


@app.get("/memos/{memo_id}")
def read_memo(memo_id: int):
    for memo in memos:
        if memo["id"] == memo_id:
            return memo
    raise HTTPException(status_code=404, detail="Memo not found")


@app.put("/memos/{memo_id}")
def update_memo(memo_id: int, updated_memo: Memo):
    for index, memo in enumerate(memos):
        if memo["id"] == memo_id:
            updated_memo_dict = updated_memo.dict()
            updated_memo_dict["id"] = memo_id
            memos[index] = updated_memo_dict
            return updated_memo_dict
    raise HTTPException(status_code=404, detail="Memo not found")


@app.delete("/memos/{memos_id}")
def delete_memo(memo_id: int):
    for index, memo in enumerate(memos):
        if memo["id"] == memo_id:
            del memos[index]
            return {"message": "Memo deleted"}
    raise HTTPException(status_code=404, detail="Memo not found")