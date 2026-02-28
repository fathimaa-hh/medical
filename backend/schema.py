from pydantic import BaseModel
from typing import Optional, List

class PatientRegister(BaseModel):
    name: str
    age: int
    blood_group: str
    allergies: Optional[str] = ""
    chronic_diseases: Optional[str] = ""
    medications: Optional[str] = ""
    emergency_contact: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    age: int
    blood_group: str
    allergies: Optional[str]
    chronic_diseases: Optional[str]
    medications: Optional[str]
    emergency_contact: str

    class Config:
        orm_mode = True

class ReportIn(BaseModel):
    patient_id: int
    hospital_name: str
    doctor_name: str
    diagnosis: str
    prescription: str

class ReportOut(BaseModel):
    diagnosis: str
    prescription: str
    report_file: Optional[str]
    date: str