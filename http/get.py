from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/view")
def view():
    return load_data()

# Path Parameters
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient Not Found")

# Query Parameters (Fixed Syntax & Typos)
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, or bmi"), 
    order: str = Query('asc', description="Sort by 'asc' or 'desc'")
): # Removed the extra closing parenthesis from this definition block

    valid_fields = ['height', 'weight', 'bmi']

    # Added 'f' for f-string formatting and fixed typos
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Select between 'asc' and 'desc'")
    
    data = load_data()

    # Determine sorting order (True for descending, False for ascending)
    sort_order = True if order == "desc" else False

    # Sort the dictionary values based on the dynamic key
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data