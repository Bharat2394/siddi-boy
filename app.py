import streamlit as st

def patient_interface():
    st.subheader("Patient Interface")
    # Add Streamlit components for patient interface
    # For example:
    patient_name = st.text_input("Enter your name")
    patient_age = st.number_input("Enter your age")
    patient_gender = st.selectbox("Select your gender", ["Male", "Female", "Other"])
    # Add more components as needed

def receptionist_interface():
    st.subheader("Receptionist Interface")
    # Add Streamlit components for receptionist interface
    # For example:
    appointment_date = st.date_input("Select appointment date")
    patient_name = st.text_input("Enter patient's name")
    # Add more components as needed

def doctor_interface():
    st.subheader("Doctor Interface")
    # Add Streamlit components for doctor interface
    # For example:
    patient_id = st.text_input("Enter patient ID")
    diagnosis = st.text_area("Enter diagnosis")
    prescription = st.text_area("Enter prescription")
    # Add more components as needed

def chemist_interface():
    st.subheader("Chemist Interface")
    # Add Streamlit components for chemist interface
    # For example:
    patient_name = st.text_input("Enter patient's name")
    medication = st.text_area("Enter prescribed medication")
    # Add more components as needed

def main():
    st.title("Hospital Management System")

    # Interface selection
    interface = st.selectbox("Select Interface", ["Patient", "Receptionist", "Doctor", "Chemist"])

    if interface == "Patient":
        patient_interface()
    elif interface == "Receptionist":
        receptionist_interface()
    elif interface == "Doctor":
        doctor_interface()
    elif interface == "Chemist":
        chemist_interface()

if __name__ == "__main__":
    main()
