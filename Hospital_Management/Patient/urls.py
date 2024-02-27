from django.urls import path
from . import views


urlpatterns =[
    path("patient-reg/", views.Registration),
    # path("patient-login/", views.patient_login),
    path("patient-prescription/", views.prescription_login),
    path('pdf/',views.pdf,name='pdf'),
]