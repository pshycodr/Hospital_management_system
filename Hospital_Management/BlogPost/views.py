from django.shortcuts import render, redirect
from django.http import HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

from django.http import JsonResponse
import base64

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


def blogUpload(request):
    try:
        doc_id = request.GET.get("doc_id")
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        current_datetime = datetime.now()
        published_date_time = current_datetime.strftime("%d-%m-%Y")

        doc_data = database.collection('Doctors Database').document(doc_id).get().to_dict()
        doc_name = doc_data.get("Basic", {}).get("full_name")
        doc_category = doc_data.get("Basic", {}).get("category")

        if title:
            key = title.lower().replace(" ", "_")

            blog_data = {
                "blog_title": title,
                "blog_content": content,
                "date_time": published_date_time,
                "publisher": doc_name,
                "category": doc_category,
                "key": key,
                "doc_id": doc_id,
            }

            # Handle image upload to Firebase Storage
            if image:
                image_data = image.read()
                image_data_url = base64.b64encode(image_data).decode('utf-8')
                
                store_image_to_firebase_storage(doc_id, image_data, key)

            database.collection('Blog Database').document(key).set(blog_data)

            return redirect(f"/blog/doc-up-blog?doc_id={doc_id}")

    except KeyError as e:
        print(f"KeyError: {e}")
        return HttpResponse("Error: Missing key in doctor's data")

    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse("Something went wrong")

    return render(request, "blog_upload.html")

def store_image_to_firebase_storage(doc_id, image_data, key):
    try:
        storage.child("Doctor Blog Images").child(f'{doc_id}/{key}.jpg').put(image_data)
        # url = storage.child("Doctor Blog Images").child(f'{doc_id}/{key}.jpg').get_url(image_data)
        # print(str(url)) 
    except Exception as e:
        print(f"Error storing image to Firebase Storage: {e}")



def doc_up_blog(request):
    
    doc_id = request.GET.get("doc_id")
    
    collection_ref = database.collection('Blog Database')
    ref_blog_key = collection_ref.stream()
    
    doc_blogs = []
    
    for blog_key in ref_blog_key:
        blogs = blog_key.to_dict()
        pub_id = blogs["doc_id"]
        if pub_id == doc_id:
            doc_blogs.append(blog_key.to_dict())

    
    
    return render(request, "doc_up_blog.html",  {"doc_blogs":doc_blogs, "doc_id":doc_id,})




def blog_edit(request):
    
    blog_key = request.GET.get("blog_key")
    print(blog_key)

    blog_data = database.collection('Blog Database').document(blog_key).get().to_dict()
    
    
    current_datetime = datetime.now()
    last_edit_date_time = current_datetime.strftime("%d-%m-%Y")

   
    blog_title = request.POST.get('title')
    blog_content = request.POST.get('content')
    
    print(blog_title)
        
    if blog_content:
        data_update = {
            "blog_title": blog_title,
            "blog_content": blog_content,
            "last_edit": last_edit_date_time,
        }
        
        print(data_update)
        
        database.collection('Blog Database').document(blog_key).update(data_update)
         
        return redirect (f'/blog/doc-up-blog/?doc_id={ blog_data["doc_id"] }')
    
    
    return render(request, "blog_edit.html", {"blog_data": blog_data} )



def all_blogs(request):
    collection_ref = database.collection('Blog Database')
    ref_blog_key = collection_ref.stream()

    blog_key = []
    blog_data = []

    for key in ref_blog_key:
        blog_key.append(key.id)
        blog_data.append(key.to_dict())
        
    

    return render(request, "all_blogs.html", { "blog_data": blog_data, "blog_key":blog_key})



def full_blog(request):

    blog_key = request.GET.get("blog_key")
    print(blog_key)

    blog_data = database.collection('Blog Database').document(blog_key).get().to_dict()
    
    
    return render(request, "full_blog.html", {"blog_data": blog_data})