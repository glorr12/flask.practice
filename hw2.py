from pydantic import BaseModel, Field, EmailStr, model_validator
import json
json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""
json_error = """{
    "name": "John Doe",
    "age": 25,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""
json_fail_address = """{
        "name": "Ivan",
        "age": 30,
        "email": "ivan@test.ru",
        "is_employed": false,
        "address": {
            "city": "Moscow",
            "street": "Arbat",
            "house_number": -5
        }
    }"""

class Adress(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0, le=120)
    email: str = Field(EmailStr)
    is_employed: bool
    address: Adress


    @model_validator(mode='after')
    def validate_age(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("Не можешь работать")
        return self

def user_registration(json_check: str):
    user = json.loads(json_check)
    User.model_validate(user)
    return json_check



try:
    print(user_registration(json_error))
except Exception as e:
    print(e)
try:
    print(user_registration(json_input))
except Exception as e:
    print(e)
try:
    print(user_registration(json_fail_address))
except Exception as e:
    print(e)