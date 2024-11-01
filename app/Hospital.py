import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd

BASE_URL = "http://localhost:8000/api"

st.sidebar.title("Navegación")
with st.sidebar:
    selected = option_menu(
        "Insertar Datos",
        ["Pacientes", "Responsables", "Diagnósticos", "Hospitales", "Citas", "Paciente-Responsable", "Subir Excel", "Consultas"],
        icons=["person-plus", "people", "clipboard-plus", "building", "calendar", "people-fill", "file-earmark-excel", "search"],
        menu_icon="cast",
        default_index=0
    )

def create_patient():
    st.title("Registrar Paciente")
    with st.form(key="patient_form"):
        first_name = st.text_input("Nombre del Paciente")
        last_name = st.text_input("Apellido del Paciente")
        diagnosis_id = st.number_input("ID del Diagnóstico", min_value=1, value=1)
        hospital_id = st.number_input("ID del Hospital", min_value=1, value=1)
        date_of_birth = st.date_input("Fecha de Nacimiento")
        submit_button = st.form_submit_button(label="Registrar Paciente")
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
                    st.success("Paciente registrado exitosamente!")
                else:
                    st.error(f"Error al registrar paciente: {response.text}")
            except requests.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def create_responsible():
    st.title("Registrar Responsable")
    with st.form(key="responsible_form"):
        name = st.text_input("Nombre del Responsable")
        relationship = st.text_input("Relación con el Paciente")
        phone = st.text_input("Teléfono", "")
        email = st.text_input("Correo Electrónico", "")
        submit_button = st.form_submit_button(label="Registrar Responsable")
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
                    st.success("Responsable registrado exitosamente!")
                else:
                    st.error(f"Error al registrar responsable: {response.text}")
            except requests.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def create_diagnosis():
    st.title("Registrar Diagnóstico")
    with st.form(key="diagnosis_form"):
        name = st.text_input("Nombre del Diagnóstico")
        submit_button = st.form_submit_button(label="Registrar Diagnóstico")
        if submit_button:
            diagnosis_data = {"name": name}
            try:
                response = requests.post(f"{BASE_URL}/diagnoses/", json=diagnosis_data)
                if response.status_code == 200:
                    st.success("Diagnóstico registrado exitosamente!")
                else:
                    st.error(f"Error al registrar diagnóstico: {response.text}")
            except requests.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def create_hospital():
    st.title("Registrar Hospital")
    with st.form(key="hospital_form"):
        name = st.text_input("Nombre del Hospital")
        address = st.text_input("Dirección del Hospital")
        city = st.text_input("Ciudad del Hospital")
        submit_button = st.form_submit_button(label="Registrar Hospital")
        if submit_button:
            hospital_data = {
                "name": name,
                "address": address,
                "city": city
            }
            try:
                response = requests.post(f"{BASE_URL}/hospitals/", json=hospital_data)
                if response.status_code == 200:
                    st.success("Hospital registrado exitosamente!")
                else:
                    st.error(f"Error al registrar hospital: {response.text}")
            except requests.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def create_appointment():
    st.title("Registrar Cita")
    with st.form(key="appointment_form"):
        patient_id = st.number_input("ID del Paciente", min_value=1)
        hospital_id = st.number_input("ID del Hospital", min_value=1)
        appointment_date = st.date_input("Fecha de la Cita")
        notes = st.text_area("Notas")
        submit_button = st.form_submit_button(label="Registrar Cita")
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
                    st.success("Cita registrada exitosamente!")
                else:
                    st.error(f"Error al registrar cita: {response.text}")
            except requests.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def create_patient_responsible():
    st.title("Registrar Relación Paciente-Responsable")
    with st.form(key="patient_responsible_form"):
        patient_id = st.number_input("ID del Paciente", min_value=1)
        responsible_id = st.number_input("ID del Responsable", min_value=1)
        submit_button = st.form_submit_button(label="Registrar Relación")
        if submit_button:
            relation_data = {
                "patient_id": patient_id,
                "responsible_id": responsible_id
            }
            try:
                response = requests.post(f"{BASE_URL}/patient-responsibles/", json=relation_data)
                if response.status_code == 200:
                    st.success("Relación registrada exitosamente!")
                else:
                    st.error(f"Error al registrar relación: {response.text}")
            except requests.RequestException as e:
                st.error(f"Error de conexión: {str(e)}")

def upload_excel():
    st.title("Subir Archivo Excel")
    uploaded_file = st.file_uploader("Elige un archivo Excel", type="xlsx")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Contenido del Archivo Excel:")
        st.dataframe(df)
        
        table_options = ["patients", "responsibles", "diagnoses", "hospitals", "appointments", "patient_responsibles"]
        selected_table = st.selectbox("Selecciona la tabla para insertar datos:", table_options)
        
        if st.button("Subir Datos"):
            if validate_dataframe(df, selected_table):
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(f"{BASE_URL}/upload-excel/?table={selected_table}", files=files)
                if response.status_code == 200:
                    st.success("Datos subidos exitosamente!")
                else:
                    st.error(f"Error al subir datos: {response.text}")
            else:
                st.error("Formato de datos no válido en el archivo Excel.")

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

def show_queries():
    st.title("Consultas")
    st.subheader("Selecciona una consulta para ejecutar:")
    
    query_options = [
        "Consulta 1: Listar todos los pacientes",
        "Consulta 2: Listar todos los responsables",
        "Consulta 3: Listar todos los diagnósticos",
        "Consulta 4: Listar todos los hospitales",
        "Consulta 5: Listar todas las citas",
        "Consulta 6: Listar pacientes por diagnóstico",
        "Consulta 7: Listar responsables por relación",
        "Consulta 8: Listar citas por paciente",
        "Consulta 9: Listar pacientes por hospital",
        "Consulta 10: Listar responsables por paciente",
        "Consulta 11: Listar hospitales por ciudad",
        "Consulta 12: Listar diagnósticos con pacientes",
        "Consulta 13: Listar citas por hospital",
        "Consulta 14: Listar pacientes sin responsables",
        "Consulta 15: Listar todas las relaciones paciente-responsable"
    ]
    
    selected_query = st.selectbox("Selecciona una consulta:", query_options)
    
    if st.button("Ejecutar Consulta"):
       
        if selected_query == "Consulta 1: Listar todos los pacientes":
            response = requests.get(f"{BASE_URL}/patients/")
            if response.status_code == 200:
                patients = response.json()
                st.write(patients)
            else:
                st.error("Error al obtener los pacientes.")
        

if selected == "Pacientes":
    create_patient()
elif selected == "Responsables":
    create_responsible()
elif selected == "Diagnósticos":
    create_diagnosis()
elif selected == "Hospitales":
    create_hospital()
elif selected == "Citas":
    create_appointment()
elif selected == "Paciente-Responsable":
    create_patient_responsible()
elif selected == "Subir Excel":
    upload_excel()
elif selected == "Consultas":
    show_queries()