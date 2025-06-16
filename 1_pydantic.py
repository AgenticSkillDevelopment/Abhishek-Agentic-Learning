from pydantic import BaseModel, Field
from typing import Optional 

class Person(BaseModel):
    name: str
    age: int
    city: str

person = Person(name="Abhishek", age=23, city="Noida")
print(person)
print(type(person))


class Employee(BaseModel):
    name: str
    age: int
    city: str
    salary: Optional[float] = None
    is_active: Optional[bool] = True

employee = Employee(name="ABHISHEK", age=23, city="NOIDA") 
print(employee)  

#nested Model

class Address(BaseModel):
    city: str
    state: str
    zip_code: int
class User(BaseModel): 
    username: str
    email: str
    address: Address

address = Address( city="New Delhi", state="Ghaziabad", zip_code=200109)
user = User(username="Abhishek", email="abhisheksingh90627@gmail.com", address=address)
print(user)


class Item(BaseModel):
    length: int = Field(ge=1, le=100)
    breadth: int = Field(ge=1, le=100)
item = Item(length=0, breadth=20)
print(item)
