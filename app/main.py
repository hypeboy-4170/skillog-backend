# app/main.py
from fastapi import FastAPI, HTTPException
from app.models import RegisterRequest
from app.auth import sign_up_user

app = FastAPI()

@app.post("/register")
async def register(req: RegisterRequest):
    try:
        resp = sign_up_user(req.email, req.password, req.name)
        return {"message": "登録完了", "userSub": resp["UserSub"], "codeDelivery": resp.get("CodeDeliveryDetails")}
    except Exception as e:
        # エラー内容をログ or レスポンスに
        raise HTTPException(status_code=400, detail=str(e))
