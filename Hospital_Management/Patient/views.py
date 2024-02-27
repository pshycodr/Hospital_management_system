from django.shortcuts import render, redirect
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

from fpdf import FPDF
import datetime

from django.http import FileResponse
import os

# Pyrebase Authentication
firebaseConfig = {
  "apiKey": "AIzaSyA81y_aBfgggpkJBLvLWZjr9NqAQMg0d_U",
  "authDomain": "hospital-management-13dbb.firebaseapp.com",
  "databaseURL": "https://hospital-management-13dbb-default-rtdb.firebaseio.com",
  "projectId": "hospital-management-13dbb",
  "storageBucket": "hospital-management-13dbb.appspot.com",
  "messagingSenderId": "884809096216",
  "appId": "1:884809096216:web:9e37288095f205c499b76d",
  "measurementId": "G-ZPQQ1FCFP9",
  "databaseURL" : "https://hospital-management-13dbb-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)     
auth = firebase.auth()



#  For Firestore
storejson={
  "type": "service_account",
  "project_id": "hospital-management-13dbb",
  "private_key_id": "84cb1ef4134ad5bec6ef80ffe42a05565c7d18d5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCubOPaCCQRWSf/\n/gZvSEZe4zL/63aq0+zkLJkxRxUIxhf1WjE+K19rGEQlbOAdwevNfwr2rFeImX3h\noWNI6l3wVptd7kCzH9P9gk2624HciP8wfKwUsywUKJhSIWh6tivlIGZLgxWXEu3x\n/3qGCmKn5Psq/Be55Uby/ONT8XJxE9l3y2BHdvO/mNxPdPmCMj7yrTSZtbS9M5hR\nFnKicFdJ3y5NUB/7yv/jf9lwfdCDFcZ0PUfCNIM4KBDwtjNhFmiNB/GVwQ1MHqGQ\noBqTKOWVE6iXKdJVPcz6iyp5aQpJb6Rdl6BDK0nXuAY8Th0LJLK6vzsZFapCrHGL\nKELC2+eFAgMBAAECggEAFZfQW0ZaZLVoq3BrToJ1h7tRAyKcsF2HpuBTNKkBPx1Q\nNk+ske7fo0vqlRwrNd6IY7ULCpTfnz7/45tNmxIR1WDQtL+meHuuYY9XMmnd4+B9\nKvz8IUc5uTh5/DeQ427C9LIJR+bZ7je/Mjq3lHlw/ipC4m7j5wpYZANk3G2jBmwY\n0e6tNTBHLCa3HI4Ni7GbxGhehA00pgXSWXxLU7j5VWHZ0g1+eA11ExDUjsZrFUy6\nqprMyMYXJy/fK4JUMVQ+yVPAHz8yJUEFXT8kwUBzh6zTswdAw/o0nnKZIo7+8svh\nOSdvk7ADglh/ew07ZJId232LDIjp+ePUOflerl3dvwKBgQDXQ/PJDPnHluiv/x/W\npQ0VoJVHl/E3TFwC9bF0tArYAFFtZ8wxeakrPo+k7aP80V8Z3q4yxfgEn3z9YUK3\nklnvoN3arjYvbU6nvT2gofzG+wDsLlivvyf5xxCCmGuTlIuLKm0tQuVmxaX4Ew1C\n6qALJ0np3g0TT6/zR+VqE6s8BwKBgQDPbogz3XK+PnlooW5GqLAHvehwoqxzSKjU\niJMlIX+l7eZ8ieJYQkfJIbm39dag8vTnfq7/KeNLbxMTlHPQVw4hKg5EGZI84/dX\nMJVYlSkg+uvNgBQoAvDkyDtgqaAFybTAZs24twdjh6kEycPpcSiSowRxg0WDnkQB\ngX4NTD81EwKBgANbXevete503gAQnHB+dmvF604Igox4Nl8dcbz+KcUgjCSGn9qN\nqSOxgA/0XMBOi4sdu92y1KFN02coIyA1ug1QluUYHmQy8i0PeGyO2iBIPcVxG5Ty\nCC+O+STwN40/ncV3zegMyQMHRgVOVsCaZBCIdlCdU9rfPUEv99XlpJ/1AoGAZ9wi\nGkXw48yIIZlii8J+kQHHVk49JmPlFLVlZ5wEO+KIGyc2y5Y0N0LJqJBQ7Ll5YkeN\n+3jPs79jv9P+wPw1uOlDx1k+XXqPJ3rN7FKTC05XrsdIUFhYoVSYVmfYFc3O0N8o\ndio+atlMCXe0vjfIZtN0sBlYPvSJfG+H28SniT0CgYBw0JlJgNeEj11IBfcvMSV9\niG2ossqSPOPgNS7qaRsDQXMR8tK2C6ioJApqT/zzMwhpy4OrJjH1YnzLv1rhZw93\n8wwogbaGnq8PiyI5OZnoUpHnCMDyuZoGAv/ey1QSop65i75I7kUvzmN9RnJhAY3w\nlk1L9E8UyzvDAnAXQcW13g==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ibcz3@hospital-management-13dbb.iam.gserviceaccount.com",
  "client_id": "104889979991036959017",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ibcz3%40hospital-management-13dbb.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
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



