from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.cognito import create_user, authenticate_user, verify_token
from services.ses import send_email

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://allforone-freesite.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

security = HTTPBearer()

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class EmailData(BaseModel):
    to: str  # フロントエンドの仕様に合わせる
    subject: str
    body: str

@app.post("/register")
async def register(user_data: UserRegister):
    try:
        create_user(user_data.username, user_data.password, user_data.email)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login") 
async def login(credentials: UserLogin):
    try:
        token = authenticate_user(credentials.username, credentials.password)
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

@app.post("/sendmail")
async def send_mail(email_data: EmailData, token: str = Depends(security)):
    if not verify_token(token.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        send_email(email_data.to, email_data.subject, email_data.body)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send email")