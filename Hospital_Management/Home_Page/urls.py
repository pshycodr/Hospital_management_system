from django.urls import path
from . import views


urlpatterns =[
    path("", views.home),
    path("homePage/", views.home),
    path("about-us/", views.about_us),
]