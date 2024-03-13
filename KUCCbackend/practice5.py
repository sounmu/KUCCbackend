from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Union


app = FastAPI()


class Memo(BaseModel):
    id: Optional[int] = None
    title: str
    content: str


class Cal(BaseModel):
    type: str
    intA: int
    intB: int


@app.post("/calculate/")
def calculate(operation: Cal):
    if operation.type == "+":
        result = operation.intA + operation.intB
    elif operation.type == "-":
        result = operation.intA - operation.intB
    elif operation.type == "*":
        result = operation.intA * operation.intB
    elif operation.type == "/":
        # 0으로 나누는 경우 예외 처리
        if operation.intB == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        result = operation.intA / operation.intB
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    return {"result": result}


memos = []


@app.post("/memos/create")
def create_memo(memo: Memo):
    memo.id = len(memos) + 1
    memos.append(memo.dict())
    return memo


@app.get("/memos/read")
def read_memos():
    return memos


@app.get("/memos/{memo_id}/read")
def read_memo(memo_id: int):
    for memo in memos:
        if memo["id"] == memo_id:
            return memo
    raise HTTPException(status_code=404, detail="Memo not found")


@app.put("/memos/{memo_id}/update")
def update_memo(memo_id: int, updated_memo: Memo):
    for index, memo in enumerate(memos):
        if memo["id"] == memo_id:
            updated_memo_dict = updated_memo.dict()
            updated_memo_dict["id"] = memo_id
            memos[index] = updated_memo_dict
            return updated_memo_dict
    raise HTTPException(status_code=404, detail="Memo not found")


@app.delete("/memos/{memos_id}/delete")
def delete_memo(memo_id: int):
    for index, memo in enumerate(memos):
        if memo["id"] == memo_id:
            del memos[index]
            return {"message": "Memo deleted"}
    raise HTTPException(status_code=404, detail="Memo not found")
