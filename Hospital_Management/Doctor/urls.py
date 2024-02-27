from django.urls import path
from . import views


urlpatterns =[
    path('doc-dashboard/', views.doc_dashboard),
    path("patients-info/", views.patients_info),
    path("doc-reg/", views.Doc_reg),
    path("doc-login/", views.Doc_login),
    path("doc-list/", views.doc_list),
    path('prescription-form/', views.prescription_form),
    path('patient-history/', views.patient_history),
    path('patient-appointmentReq/', views.appointments_req),
    
]