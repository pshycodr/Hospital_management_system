from django.shortcuts import render, redirect
from django.http import HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import jinja2
from jinja2 import Environment, FileSystemLoader

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
storage = firebase.storage()




# Create your views here.

# Doctor Reistration
def Doc_reg(request):
    # Basic
    first_Name = request.POST.get("first_name")
    # middle_Name = request.POST.get("middle_name")
    last_Name = request.POST.get("Last_name")
    profile_img = request.FILES.get("doc_profile_img")
    
    email= request.POST.get("email")
    password =  request.POST.get("Password")
    
    doc_data = {
    "Basic": {
        "full_name": str(request.POST.get("first_name")).capitalize() + ' ' + str(request.POST.get("Last_name")).capitalize(),
        "doc_dob": request.POST.get("doc_dob"),
        "gender": request.POST.get("gender"),
        "category": request.POST.get("Category"),
        "appointment_date": request.POST.get("appointment_date"),

        "email": request.POST.get("email"),
        "Password": request.POST.get("Password"),
    },
    "SSC_exam": {
        "inst_name": request.POST.get("SSC_inst_name"),
        "year": request.POST.get("SSC_year"),
        "div_cgpa": request.POST.get("SSC_div_cgpa"),
        "position": request.POST.get("SSC_position"),
        "certificate": request.POST.get("SSC_certificate")
    },
    "HSC_exam": {
        "inst_name": request.POST.get("HSC_inst_name"),
        "year": request.POST.get("HSC_year"),
        "div_cgpa": request.POST.get("HSC_div_cgpa"),
        "position": request.POST.get("HSC_position"),
        "certificate": request.POST.get("HSC_certificate")
    },
    "MBBS_exam": {
        "inst_name": request.POST.get("MBBS_inst_name"),
        "year": request.POST.get("MBBS_year"),
        "div_cgpa": request.POST.get("MBBS_div_cgpa"),
        "position": request.POST.get("MBBS_position"),
        "certificate": request.POST.get("MBBS_certificate")
    },
  }
    job_experience=[]
    for i in range(1,6):
        if request.POST.get(f"job_desg_{i}") == "":
            break;
        else:
            experience={
                "job_desg": request.POST.get(f"job_desg_{i}"),
                "from": request.POST.get(f"from_{i}"),
                "to": request.POST.get(f"to_{i}"),
                "org_name": request.POST.get(f"org_name_{i}"),
            }
            job_experience.append(experience)
            
        doc_data["job_experience"] = job_experience
        
  
    try:

        token= auth.create_user_with_email_and_password(email, password)


        database.collection('Doctors Database').document(email).set(doc_data)


        storage.child("Doctor Profile Images").child(f'{email}/profile.jpg').put(profile_img)
        url = storage.child("Doctor Profile Images").child(f'{email}/profile.jpg').get_url(token['idToken'])
        print(str(url)) 




    except:
        print("Something Went Wrong!!!")

  

    return render(request, "doc_reg.html")
  

# Doctor Login to their DashBoard
def Doc_login(request):
    
    email = request.POST.get("Doc_id")
    password = request.POST.get("password")
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Success")
        
        return redirect(f"/doctor/doc-dashboard?doc_id={email}")
    
    except:
        print("somethis is wrong")
    
    return render (request, "doc_login.html")



# Doctors Dashboard 
def doc_dashboard(request):
    doc_id = request.GET.get("doc_id")
    return render(request, "doctor_dashbord.html", {"doc_id":doc_id})



# Appointment Requests from Patients
def appointments_req(request):

    doc_id = request.GET.get("doc_id")
    
    collection_ref = database.collection('Patients Database')

    docs = collection_ref.stream()
    pat_id=[]
    data=[]
    for doc in docs:  
        pat_id.append(doc.id)
        data.append(doc.to_dict()) 
        
    # Appointment approval email

    appointmentDateTime_ISO = request.POST.get("appointmentDateTime")
    
    if appointmentDateTime_ISO:
        appointment_datetime_obj = datetime.fromisoformat(str(appointmentDateTime_ISO))
        appointmentDateTime = appointment_datetime_obj.strftime("%d-%m-%Y %H:%M:%S")
        patient_id = request.POST.get("patient_id")
        print(patient_id)
        
        patient_data = database.collection("Patients Database").document(patient_id).get().to_dict()

        print(patient_data)
        if appointmentDateTime:
            patient_email = patient_data["Email"]
            print(patient_email)
            print(f"Appointment Done on date {appointmentDateTime}")
            print(patient_email)

            smtpObject = s.SMTP("smtp.gmail.com", 587)
            From = os.getenv('EMAIL_ID')
            Password = os.getenv('EMAIL_KEY')

            smtpObject.starttls()
            smtpObject.login(From, Password)

            template_loader = FileSystemLoader(searchpath="static")
            jinja_env = Environment(loader=template_loader)

            template = jinja_env.get_template("appointment_mail.html")

            html_content = template.render(patient_data=patient_data, appointmentDateTime=appointmentDateTime)

            msg = MIMEMultipart()
            msg.attach(MIMEText(html_content, 'html'))

            msg['From'] = From
            msg['To'] = patient_email
            msg['Subject'] = "Appointment Approval"

            smtpObject.sendmail(From, patient_email, msg.as_string())
            smtpObject.quit()
            
            
            # Adding Patients info to prescription database
            
            pat_info = {
                "patients_info":patient_data,
                "Appointment_date": appointmentDateTime,
            }
            database.collection('Prescription Database').document(patient_id).set(pat_info)
                    
    
    appointment_requests = []
    for app_data in data:
        appointed_doc_id = app_data.get('appointed_doc', {}).get('doc_id', None)
        
        if appointed_doc_id == doc_id:
            appointment_requests.append(app_data)

    if appointment_requests:
        return render(request, "appointments_req.html", {"pat_ids": pat_id, "data": appointment_requests})
    else:
        return HttpResponse("No Appointment Requests")


# Prescription Fill up
def prescription_form(request):
    
    pid = request.GET.get("pid")
    patient_data = database.collection("Patients Database").document(pid).get().to_dict()
    print(patient_data)
    
    if request.method == 'POST':
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d-%m-%y %H:%M:%S")
        prescription_data = {}


        prescription_data['Diagnested_with'] = request.POST.get("Diagnested_with")
        prescription_data['advice_time']=formatted_datetime
        
        # pat_id = prescription_data['pat_id']

        # Medicines Prescribed
        medicines_prescribed = []
        for i in range(1, 6):
            
            if request.POST.get(f"med_id_{i}") == "":
                break;
            else:
                med_dict = {
                    "med_id": request.POST.get(f"med_id_{i}"),
                    "med_name": request.POST.get(f"med_name_{i}"),
                    "quantity": request.POST.get(f"quantity_{i}"),
                    "morning": request.POST.get(f"time_morning_{i}"),
                    "afternoon": request.POST.get(f"time_afternoon_{i}"),
                    "night": request.POST.get(f"time_night_{i}"),
                }
                medicines_prescribed.append(med_dict)
            
            prescription_data['medicines_prescribed'] = medicines_prescribed

        # Test Advices
        test_advices = []
        for i in range(1, 4):
            if request.POST.get(f"test_id_{i}") == "":
                break;

            else:
                test_dict = {
                    "test_id": request.POST.get(f"test_id_{i}"),
                    "test_name": request.POST.get(f"test_name_{i}"),
                    "test_Instructions": request.POST.get(f"Instructions_{i}"),
                }
                test_advices.append(test_dict)

            prescription_data['test_advices'] = test_advices

        prescription_data['special_notes_restrictions'] = request.POST.get("comments")
        prescription_data['doc_id'] = request.POST.get("doc_id")
        prescription_data['doc_name'] = request.POST.get("doc_name")

        print("Prescription Data:")
        print(prescription_data)
            
        try:
            database.collection('Prescription Database').document(pid).update({"prescription_data":prescription_data})
            # database.collection('Patients Database').document(pid).update({"prescription_data":prescription_data})
            return HttpResponse("Prescription submitted successfully!")

            
        except:
            print("Something Went Wrong!!!")


    return render(request, 'prescription_form.html', {"patient_data":patient_data})



# List of patients under each Doctor
def patients_info(request):
    
    doc_id = request.GET.get("doc_id")
    collection_ref = database.collection('Prescription Database')

    docs = collection_ref.stream()
    pat_id=[]
    data=[]
    for doc in docs: 
        if doc == doc_id: 
            pat_id.append(doc.id)
            data.append(doc.to_dict())
    print(data)
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y %H:%M:%S")
    
    return render(request, "patients_info.html", {"pat_ids": pat_id, "data":data, "current_datetime": formatted_datetime})



# Patients Medical History
def patient_history(request):
    pat_id = request.GET.get("pid")
    data = database.collection('Prescription Database').document(pat_id).get().to_dict()
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y %H:%M:%S")
    
    
    return render(request, "patient_medi_history.html", {"pres_data":data, "current_datetime":formatted_datetime})



# Doctor list for patients to Book Appointment
def doc_list(request):
    docs_list = database.collection("Doctors Database").stream()
    doc_id = []
    doc_data=[]
    for doc in docs_list:
        doc_id.append(doc.id)
        doc_data.append(doc.to_dict())
        
    # url = storage.child("Doctor Profile Images").child(f'{email}/profile.jpg').get_url(token['idToken'])

        
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%y %H:%M:%S")
    return render(request, "docs_list.html", {"doc_id":doc_id, "doc_data":doc_data, "current_datetime": formatted_datetime})


