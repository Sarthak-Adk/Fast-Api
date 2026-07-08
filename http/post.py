from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, computed_field
import json
from typing import Annotated, Literal

app = FastAPI()

def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_data(data):
    try:
        with open('patients.json','w') as f:
            json.dump(data,f)
    except FileNotFoundError:
        return{}

class Patient(BaseModel):

    id : Annotated[str, Field(..., description = "ID og the Patient", examples=["P001"])]
    name :  Annotated[str, Field(..., description = "Name of the Patient")]
    city :  Annotated[str, Field(..., description = "City of the Patient")]
    age :   Annotated[int, Field(..., gt=0,lt=120 ,description = "Age of the Patient")]
    gender :  Annotated[Literal['male','female','other'],Field(..., description = "City of the Patient")]
    height : Annotated[float, Field(..., gt=0, description = "Height of the Patient")]
    weight : Annotated[float, Field(..., gt=0, description = "Weight of the Patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "overweight"
        else:
            return "Obese"
        

@app.post("/create")
def create_function( patient: Patient):
    
    #load existing data
    data = load_data()

    #check the data is already exit 
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient is aleady exit")

    #new patient add to the database
    data[patient.id] = patient.model_dump(exclude =["id"])

    #save this to json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient create successfully'})