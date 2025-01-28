from django.shortcuts import render, redirect
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

from fpdf import FPDF
import datetime

from django.http import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()


# Pyrebase Authentication
firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")  
}

firebase = pyrebase.initialize_app(firebaseConfig)     
auth = firebase.auth()



# For Firestore
storejson = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}

cred = credentials.Certificate(storejson)
if not firebase_admin._apps:
  firebase_admin.initialize_app(cred)

database = firestore.client()





# Create your views here.

def Registration(request):
    first_Name = request.POST.get("firstName")
    last_Name = request.POST.get("lastName")
    dob = request.POST.get("dob")
    gender = request.POST.get("gender")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    blood_Group = request.POST.get("bloodGroup")
    desc_problem = request.POST.get("desc_problem")

    full_Name = str(first_Name).capitalize() +' '+ str(last_Name).capitalize()
    
    patient_id = str(first_Name) + str(dob) + str(phone)[:5]
    
    
    
    # Appointed Doctor's info
    doc_id = request.GET.get("d_id")
    doc_data = database.collection('Doctors Database').document(doc_id).get().to_dict()
    doc_name = str(doc_data["Basic"]["full_name"])
    doc_catagory = str(doc_data["Basic"]["category"])
    doc_email = str(doc_data["Basic"]["email"])
    
    app_doc_info = {
      "doc_id" : doc_id,
      "doc_name": doc_name,
      "doc_catagory" : doc_catagory,
      "doc_email" : doc_email,
    }
    

    patients_data= {"Full_Name":full_Name, "Gender":gender, "Date_of_Birth":dob, "Phone_Number":phone, "Address":address, "Blood_Group":blood_Group, "desc_problem":desc_problem, "Email": email, "pid":patient_id , "appointed_doc": app_doc_info}

    try:
        # auth.create_user_with_email_and_password(email, password)

        database.collection('Patients Database').document(patient_id).set(patients_data)

        print(patients_data)
        print("Success!!")
        print(f"your patient id is ------------->>>>  {patient_id}")
        
    except:
       print("Something Went Wrong!!!")


    return render(request, "P_registration.html")
  

  
  
def prescription_login(request):
  
    pat_id = request.POST.get("patient_id")
    data = database.collection('Prescription Database').document(pat_id).get().to_dict()
    print(data)
    if data:
        return render(request, "prescription.html", {"prescription_data": data,"patient_id":pat_id})
        # return redirect( "http://127.0.0.1:8000/patient/pdf/", {"patient_id": patient_id})
        print("it is ok")

    return render(request, "patient_login.html")
  


# Function to add data to PDF dynamically in a table
def pdf(request):
    
    patient_id = request.GET.get("P")
    data = database.collection('Prescription Database').document(patient_id).get().to_dict()

    pdf = FPDF()
    pdf.add_page()
    
      # Load hospital logo
    hospital_logo_path = 'static/logo.png'
    pdf.image(hospital_logo_path, x=160, y=8, w=30)  

    # Set font for section titles
    pdf.set_font("Arial", size=14, style='B')

    # Hospital name (centered)
    pdf.cell(0, 10, txt="ZenCare Health Center  ", ln=True, align='C')

    # Doctor details
    pdf.ln(10)  # Add some space
    pdf.cell(0, 8, txt="Doctor Name: " + data['prescription_data']['doc_name'], ln=True)
    pdf.cell(0, 8, txt="Doctor ID: " + data['prescription_data']['doc_id'], ln=True)

    # Patient details
    pdf.ln(10)
    pdf.cell(0, 8, txt="Patient ID: " + data['patients_info']['pid'], ln=True)
    pdf.cell(0, 8, txt="Patient Name: " + data['patients_info']['Full_Name'], ln=True)

    # Medications table
    pdf.ln(15)
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, txt="Medications Prescribed:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(30, 10, "Medication", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Dosage", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Morning", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Afternoon", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Night", 1, 1, 'C', fill=True)

    for med in data['prescription_data']['medicines_prescribed']:
        pdf.cell(30, 10, med['med_name'], 1)
        pdf.cell(30, 10, str(med['quantity']), 1)
        pdf.cell(30, 10, med['morning'], 1)
        pdf.cell(30, 10, med['afternoon'], 1)
        pdf.cell(30, 10, med['night'], 1)
        pdf.ln()

    # Tests table
    pdf.ln(10)
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, txt="Tests Advised:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(20, 10, "Test ID", 1, 0, 'C', fill=True)
    pdf.cell(40, 10, "Test Name", 1, 0, 'C', fill=True)
    # pdf.cell(25, 10, "Date", 1, 0, 'C', fill=True)
    # pdf.cell(25, 10, "Time", 1, 0, 'C', fill=True)
    pdf.cell(60, 10, "Instructions", 1, 1, 'C', fill=True)

    for test in data['prescription_data']['test_advices']:
        pdf.cell(20, 10, test['test_id'], 1)
        pdf.cell(40, 10, test['test_name'], 1)
        # pdf.cell(25, 10, data['advice_time'][0:10], 1)
        # pdf.cell(25, 10, data['advice_time'][11:16], 1)
        pdf.cell(60, 10, test['test_Instructions'], 1)
        pdf.ln()

    pdf_name = data['patients_info']['pid']
    pdf_output_path = 'A:\Django\Hospital_management-main\Hospital_management-main\Hospital_Management' + pdf_name + '_prescription.pdf'

    pdf.output(pdf_output_path)
    with open(pdf_output_path, 'rb') as pdf_file:
      response = FileResponse(pdf_file, as_attachment=True, filename=f'{pdf_name}_prescription.pdf')

    print(f'PDF saved')
    return render(request, "prescription.html", {"prescription_data": data, "patient_id": patient_id})



