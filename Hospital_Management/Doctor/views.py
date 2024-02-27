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



# For Firestore
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
            From = "aroy262692@gmail.com"
            Password = "byul izrf kzlj qlib"

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


