from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

class DiagnosisCreate(BaseModel):
    name: str

class Diagnosis(DiagnosisCreate):
    id: int

class HospitalCreate(BaseModel):
    name: str
    address: str
    city: str

class Hospital(HospitalCreate):
    id: int

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    diagnosis_id: Optional[int]
    hospital_id: Optional[int]
    date_of_birth: Optional[date]

class Patient(PatientCreate):
    id: int

class ResponsibleCreate(BaseModel):
    name: str
    relationship: str
    phone: Optional[str]
    email: Optional[EmailStr]

class Responsible(ResponsibleCreate):
    id: int

class AppointmentCreate(BaseModel):
    patient_id: int
    hospital_id: int
    appointment_date: date
    notes: Optional[str] = None

class Appointment(AppointmentCreate):
    id: int

class PatientResponsible(BaseModel):
    patient_id: int
    responsible_id: int
