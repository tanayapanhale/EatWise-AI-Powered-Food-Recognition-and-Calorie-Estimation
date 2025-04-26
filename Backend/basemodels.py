from pydantic import BaseModel, EmailStr
from typing import Union

class userCredentialsFormat(BaseModel):
    name: str
    email: Union[str, int]
    password: Union[str, int]

class LoginFormat(BaseModel):
    email: str
    password: str

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

class FoodHistory(BaseModel):
    start_date:str 
    end_date:str