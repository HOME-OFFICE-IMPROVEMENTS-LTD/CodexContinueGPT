from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"message": "👋 Hello from /hello route!"}
@router.get("/goodbye")
def say_goodbye():
    return {"message": "👋 Goodbye from /goodbye route!"}