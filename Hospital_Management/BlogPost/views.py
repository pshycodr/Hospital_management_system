from django.shortcuts import render, redirect
from django.http import HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

from django.http import JsonResponse
import base64



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