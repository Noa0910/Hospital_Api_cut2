from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.database import get_db_connection
from app.models import (
    PatientCreate, Patient, ResponsibleCreate, Responsible, 
    DiagnosisCreate, Diagnosis, HospitalCreate, Hospital, 
    AppointmentCreate, Appointment, PatientResponsible
)
import pandas as pd
import io

router = APIRouter()

@router.post("/patients/", response_model=Patient)
def create_patient(patient: PatientCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, diagnosis_id, hospital_id, responsible_id, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient.first_name, patient.last_name, patient.diagnosis_id, patient.hospital_id, patient.responsible_id, patient.date_of_birth))
    connection.commit()
    patient_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"id": patient_id, **patient.dict()})

@router.post("/responsibles/", response_model=Responsible)
def create_responsible(responsible: ResponsibleCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO responsibles (name, relationship, phone, email)
        VALUES (%s, %s, %s, %s)
        """, (responsible.name, responsible.relationship, responsible.phone, responsible.email))
    connection.commit()
    responsible_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"id": responsible_id, **responsible.dict()})

@router.post("/diagnoses/", response_model=Diagnosis)
def create_diagnosis(diagnosis: DiagnosisCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO diagnoses (name)
        VALUES (%s)
        """, (diagnosis.name,))
    connection.commit()
    diagnosis_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"id": diagnosis_id, **diagnosis.dict()})

@router.post("/hospitals/", response_model=Hospital)
def create_hospital(hospital: HospitalCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO hospitals (name, address, city)
        VALUES (%s, %s, %s)
        """, (hospital.name, hospital.address, hospital.city))
    connection.commit()
    hospital_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"id": hospital_id, **hospital.dict()})

@router.post("/appointments/", response_model=Appointment)
def create_appointment(appointment: AppointmentCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_id, hospital_id, responsible_id, appointment_date, notes)
        VALUES (%s, %s, %s, %s, %s)
        """, (appointment.patient_id, appointment.hospital_id, appointment.responsible_id, appointment.appointment_date, appointment.notes))
    connection.commit()
    appointment_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"id": appointment_id, **appointment.dict()})

@router.post("/patient-responsibles/")
def create_patient_responsible(patient_responsible: PatientResponsible):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO patient_responsible (patient_id, responsible_id)
        VALUES (%s, %s)
        """, (patient_responsible.patient_id, patient_responsible.responsible_id))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"message": "Relationship created successfully."})

@router.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...), table: str = None):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        connection = get_db_connection()
        cursor = connection.cursor()
        if table not in ["patients", "responsibles", "diagnoses", "hospitals", "appointments", "patient_responsibles"]:
            raise HTTPException(status_code=400, detail="Invalid table.")
        if table == "patients":
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO patients (first_name, last_name, diagnosis_id, hospital_id, responsible_id, date_of_birth)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (row['first_name'], row['last_name'], row['diagnosis_id'], row['hospital_id'], row['responsible_id'], row['date_of_birth']))
        elif table == "responsibles":
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO responsibles (name, relationship, phone, email)
                    VALUES (%s, %s, %s, %s)
                """, (row['name'], row['relationship'], row['phone'], row['email']))
        elif table == "diagnoses":
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO diagnoses (name)
                    VALUES (%s)
                """, (row['name'],))
        elif table == "hospitals":
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO hospitals (name, address, city)
                    VALUES (%s, %s, %s)
                """, (row['name'], row['address'], row['city']))
        elif table == "appointments":
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO appointments (patient_id, hospital_id, responsible_id, appointment_date, notes)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row['patient_id'], row['hospital_id'], row['responsible_id'], row['appointment_date'], row.get('notes')))
        elif table == "patient_responsibles":
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO patient_responsible (patient_id, responsible_id)
                    VALUES (%s, %s)
                """, (row['patient_id'], row['responsible_id']))
        connection.commit()
        cursor.close()
        connection.close()
        return JSONResponse(status_code=200, content={"message": "Data uploaded successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
