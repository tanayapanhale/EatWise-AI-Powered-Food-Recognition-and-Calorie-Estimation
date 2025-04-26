from fastapi import FastAPI, Form, Response, Request, Depends
from fastapi import UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import database_operations as db
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI
from pytz import timezone
from pathlib import Path
from basemodels import *
import model_prediction
import send_mail 
import calories
import tempfile
import uvicorn
import dotenv
import json
import glob
import os

dotenv.load_dotenv()

indian_time = timezone('Asia/Kolkata')
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/styles", StaticFiles(directory="../Frontend/styles"), name="css")
app.mount("/scripts", StaticFiles(directory="../Frontend/scripts"), name="js")
app.mount("/pages", StaticFiles(directory="../Frontend/pages"), name="pages")
app.mount("/assets", StaticFiles(directory="../Frontend/assets"), name="assets")
templates = Jinja2Templates(directory="../Frontend/pages")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def user_authentication(response:Response, request: Request):
    session_token = request.cookies.get("authorized_user")
    if not session_token:
        response.delete_cookie("authorized_user")
        raise HTTPException(status_code=401, detail="Unauthorized! Please login.")
    session = db.check_user_by_session(session_token)
    if not session:
        db.delete_user(session_token)
        response.delete_cookie(key="authorized_user")
        raise HTTPException(status_code=401, detail="Invalid session! Please login again.")
    return session["email"]

def get_latest_detected_image():
    folder_path = Path("Detects")
    # Get all subdirectories inside "Detects" (like predict1, predict2, ...)
    subdirs = [d for d in folder_path.iterdir() if d.is_dir()]
    if not subdirs:
        return None
    # Find the latest prediction subdirectory based on modification time
    latest_subdir = max(subdirs, key=lambda d: d.stat().st_mtime)
    # Get all image files in the latest prediction folder
    image_files = list(latest_subdir.glob("*.jpg")) + list(latest_subdir.glob("*.png")) + list(latest_subdir.glob("*.jpeg"))
    if not image_files:
        return None
    # Get the most recently modified image file
    latest_image = max(image_files, key=lambda f: f.stat().st_mtime)
    return latest_image

@app.get("/eatwise")
def eatwise(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.exception_handler(404)
async def exception_handle(request:Request, error):
    return templates.TemplateResponse(request=request, name="error_404.html")

@app.post("/register")
async def register_credentials(data:userCredentialsFormat,token: Annotated[str, Depends(oauth2_scheme)]):
    if token == os.getenv('REGISTER_API_TOKEN'):
        if db.check_user_by_email(data.email):
            raise HTTPException(405, detail="Email already exists. Please try with a different email.")
        else:
            db.insert_user(data.name,data.email,data.password)
            return {"message": "Registration Successful!"}
    else:
        raise HTTPException(403, detail="Invalid API Token")

@app.post("/login")
async def login_credentials(data:LoginFormat, response:Response,token: Annotated[str, Depends(oauth2_scheme)]):
    if token == os.getenv('LOGIN_API_TOKEN'):
        user = db.check_user_by_email_and_password(data.email,data.password)
        if user:
            session_token = os.urandom(128).hex()
            db.update_user_session(data.email,session_token)
            response.set_cookie(key="authorized_user", value=session_token)
            return {"message": "Logged in Successfully!"}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password!")
    else:
        raise HTTPException(403, detail="Invalid API Token")

@app.post("/recognize")
async def recognize_food(response:Response, request: Request, token: Annotated[str, Depends(oauth2_scheme)], image: UploadFile = File(...)):
    if token == os.getenv('RECOGNIZE_API_TOKEN'):
        user_authentication(response, request)
        name = image.filename
        with tempfile.NamedTemporaryFile(suffix=f'.{name.split(".")[-1]}',delete=False) as temp:
            temp.write(await image.read())
            temp_path = temp.name
        temp.close()
        detected_items = model_prediction.get_model_recognitions(temp_path)
        latest_image = get_latest_detected_image()   # Returns the latest detected image as an HTTP response
        if latest_image:
            return FileResponse(latest_image, media_type="image/jpeg/jpg", filename=latest_image.name)  # Serving the image
        else:
            raise HTTPException(status_code=404, detail="No detected image found!")
    else:
        raise HTTPException(403, detail="Invalid API Token")

@app.post("/predict")
async def post_image(response:Response, request: Request, token: Annotated[str, Depends(oauth2_scheme)], image: UploadFile = File(...)):
    if token == os.getenv('PREDICT_API_TOKEN'):
        emailid = user_authentication(response, request)
        name = image.filename
        with tempfile.NamedTemporaryFile(suffix=f'.{name.split(".")[-1]}',delete=False) as temp:
            temp.write(await image.read())
            temp_path = temp.name   
        temp.close()
        detected_items = model_prediction.get_model_predictions(temp_path)
        detail_food = []
        for i in detected_items:
            data = json.loads(calories.get_items(i))
            data['email'] = emailid
            data['Date'] = datetime.now(indian_time).strftime("%Y-%m-%d")
            data['Time'] = datetime.now(indian_time).strftime("%I:%M %p")
            data_entry = db.insert_history_data(data)
            del data['_id']
            detail_food.append(data)
        print(detail_food)
        return detail_food
    else:
        raise HTTPException(403, detail="Invalid API Token")

@app.post("/food_history") 
async def get_food_history(data:FoodHistory, request: Request, response: Response, token: Annotated[str, Depends(oauth2_scheme)]):
    if token == os.getenv('HISTORY_API_TOKEN'):
        email = user_authentication(response, request)
        food_history_data = db.find_history_user(email, data.start_date, data.end_date)
        food_history_data = list(food_history_data)
        for food_data in food_history_data:
            del food_data["email"]
        return food_history_data
    else:
        raise HTTPException(403, detail="Invalid API Token")

@app.post("/send_email")
async def send_contact_email(data: ContactForm, token: Annotated[str, Depends(oauth2_scheme)]):
    send_mail.send_email_to_you(data)
    send_mail.send_email_to_user(data)
    return {"message": "Emails sent successfully!"}

@app.get("/logout")
async def logout_user(request: Request, response: Response):
    session_token = request.cookies.get("authorized_user")
    if session_token:
        response.delete_cookie(key="authorized_user")
        return {"message": "Logged out successfully!"}
    else:
        raise HTTPException(status_code=404, detail="No active session found!")   

if __name__ == "__main__":
    uvicorn.run("main:app", port=8888, reload=True)
