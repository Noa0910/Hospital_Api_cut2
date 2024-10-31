import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd

BASE_URL = "http://localhost:8000/api"

st.sidebar.title("Navigation")
with st.sidebar:
    selected = option_menu(
        "Insert Data",
        ["Patients", "Responsibles", "Diagnoses", "Hospitals", "Appointments", "Patient-Responsible", "Upload Excel"],
        icons=["person-plus", "people", "clipboard-plus", "building", "calendar", "people-fill", "file-earmark-excel"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Patients":
    st.title("Register Patient")
    with st.form(key="patient_form"):
        first_name = st.text_input("Patient's First Name")
        last_name = st.text_input("Patient's Last Name")
        diagnosis_id = st.number_input("Diagnosis ID", min_value=1)
        hospital_id = st.number_input("Hospital ID", min_value=1)
        date_of_birth = st.date_input("Date of Birth")
        submit_button = st.form_submit_button(label="Register Patient")
        if submit_button:
            patient_data = {
                "first_name": first_name,
                "last_name": last_name,
                "diagnosis_id": diagnosis_id,
                "hospital_id": hospital_id,
                "date_of_birth": str(date_of_birth)
            }
            try:
                response = requests.post(f"{BASE_URL}/patients/", json=patient_data)
                if response.status_code == 200:
                    st.success("Patient registered successfully!")
                else:
                    st.error(f"Error registering patient: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

elif selected == "Responsibles":
    st.title("Register Responsible")
    with st.form(key="responsible_form"):
        name = st.text_input("Responsible's Name")
        relationship = st.text_input("Relationship to Patient")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        submit_button = st.form_submit_button(label="Register Responsible")
        if submit_button:
            responsible_data = {
                "name": name,
                "relationship": relationship,
                "phone": phone,
                "email": email
            }
            try:
                response = requests.post(f"{BASE_URL}/responsibles/", json=responsible_data)
                if response.status_code == 200:
                    st.success("Responsible registered successfully!")
                else:
                    st.error(f"Error registering responsible: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

elif selected == "Diagnoses":
    st.title("Register Diagnosis")
    with st.form(key="diagnosis_form"):
        name = st.text_input("Diagnosis Name")
        submit_button = st.form_submit_button(label="Register Diagnosis")
        if submit_button:
            diagnosis_data = {"name": name}
            try:
                response = requests.post(f"{BASE_URL}/diagnoses/", json=diagnosis_data)
                if response.status_code == 200:
                    st.success("Diagnosis registered successfully!")
                else:
                    st.error(f"Error registering diagnosis: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

elif selected == "Hospitals":
    st.title("Register Hospital")
    with st.form(key="hospital_form"):
        name = st.text_input("Hospital Name")
        address = st.text_input("Address")
        city = st.text_input("City")
        submit_button = st.form_submit_button(label="Register Hospital")
        if submit_button:
            hospital_data = {
                "name": name,
                "address": address,
                "city": city
            }
            try:
                response = requests.post(f"{BASE_URL}/hospitals/", json=hospital_data)
                if response.status_code == 200:
                    st.success("Hospital registered successfully!")
                else:
                    st.error(f"Error registering hospital: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

elif selected == "Appointments":
    st.title("Register Appointment")
    with st.form(key="appointment_form"):
        patient_id = st.number_input("Patient ID", min_value=1)
        hospital_id = st.number_input("Hospital ID", min_value=1)
        appointment_date = st.date_input("Appointment Date")
        notes = st.text_area("Notes")
        submit_button = st.form_submit_button(label="Register Appointment")
        if submit_button:
            appointment_data = {
                "patient_id": patient_id,
                "hospital_id": hospital_id,
                "appointment_date": str(appointment_date),
                "notes": notes
            }
            try:
                response = requests.post(f"{BASE_URL}/appointments/", json=appointment_data)
                if response.status_code == 200:
                    st.success("Appointment registered successfully!")
                else:
                    st.error(f"Error registering appointment: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

elif selected == "Patient-Responsible":
    st.title("Register Patient-Responsible Relationship")
    with st.form(key="patient_responsible_form"):
        patient_id = st.number_input("Patient ID", min_value=1)
        responsible_id = st.number_input("Responsible ID", min_value=1)
        submit_button = st.form_submit_button(label="Register Relationship")
        if submit_button:
            relation_data = {
                "patient_id": patient_id,
                "responsible_id": responsible_id
            }
            try:
                response = requests.post(f"{BASE_URL}/patient-responsibles/", json=relation_data)
                if response.status_code == 200:
                    st.success("Relationship registered successfully!")
                else:
                    st.error(f"Error registering relationship: {response.text}")
            except requests.RequestException as e:
                st.error(f"Connection error: {str(e)}")

elif selected == "Upload Excel":
    st.title("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Excel File Content:")
        st.dataframe(df)
        table_options = ["patients", "responsibles", "diagnoses", "hospitals", "appointments", "patient_responsibles"]
        selected_table = st.selectbox("Select the table to insert data:", table_options)
        if st.button("Upload Data"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(f"{BASE_URL}/upload-excel/?table={selected_table}", files=files)
            if response.status_code == 200:
                st.success("Data uploaded successfully!")
            else:
                st.error(f"Error uploading data: {response.text}")

def validate_dataframe(df, table_name):
    if table_name == "diagnoses":
        return set(df.columns) == {"name"}
    elif table_name == "hospitals":
        return set(df.columns) == {"name", "address", "city"}
    elif table_name == "patients":
        return set(df.columns) == {"first_name", "last_name", "diagnosis_id", "hospital_id", "date_of_birth"}
    elif table_name == "responsibles":
        return set(df.columns) == {"name", "relationship", "phone", "email"}
    elif table_name == "appointments":
        return set(df.columns) == {"patient_id", "hospital_id", "appointment_date", "notes"}
    elif table_name == "patient_responsibles":
        return set(df.columns) == {"patient_id", "responsible_id"}
    return False
