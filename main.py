from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv

app = FastAPI()

# Enable CORS for all origins (allow GET requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Global variable to store student data after loading
students = []

# Load CSV data when app starts
@app.on_event("startup")
def load_data():
    global students
    with open("q-fastapi.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        students = []
        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })

@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    """
    If no class filter, return all students.
    If classes specified, filter and return students whose class is in the filter list.
    Preserve the order of students as in CSV.
    """
    if class_:
        filtered_students = [s for s in students if s["class"] in class_]
        return {"students": filtered_students}
    return {"students": students}

# Add this root route to avoid 404 on base URL
@app.get("/")
def root():
    return {"message": "FastAPI app is live!"}
