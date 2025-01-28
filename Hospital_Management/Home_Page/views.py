from django.shortcuts import render

import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jinja2
from jinja2 import Environment, FileSystemLoader

import os
from dotenv import load_dotenv

load_dotenv()


# Create your views here.

def home(request):
  
    patient_name = request.POST.get("patient_name")
    patient_email = request.POST.get("patient_email")
    patient_problem = request.POST.get("patient_problem")
    
    if patient_name:
        smtpObject = s.SMTP("smtp.gmail.com", 587)
        From = os.getenv('EMAIL_ID')
        Password = os.getenv('EMAIL_KEY')

        print(From, Password)
        
        smtpObject.starttls()
        smtpObject.login(From, Password)

        template_loader = FileSystemLoader(searchpath="static")
        jinja_env = Environment(loader=template_loader)

        template = jinja_env.get_template("online_consultaion.html")

        html_content = template.render(patient_name=patient_name, patient_problem=patient_problem)

        msg = MIMEMultipart()
        msg.attach(MIMEText(html_content, 'html'))

        msg['From'] = From
        msg['To'] = patient_email
        msg['Subject'] = "Consultation Request Confirmation"

        smtpObject.sendmail(From, patient_email, msg.as_string())
        smtpObject.quit()

    return render (request, "index.html")



def about_us(request):
    
    return render(request, "about_us.html")