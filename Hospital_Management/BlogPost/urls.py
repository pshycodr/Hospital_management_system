from django.urls import path
from . import views


urlpatterns = [
    path("Blog-upload/",  views.blogUpload),
    path("all-blogs/",  views.all_blogs),
    path("full-blog/",  views.full_blog),
    path("doc-up-blog/",  views.doc_up_blog),
    path("blog-edit/",  views.blog_edit),
]
