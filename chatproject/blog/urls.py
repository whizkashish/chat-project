# urls.py

from django.urls import path
from .views import blog_list,cat_blog_list, blog_detail, import_csv
urlpatterns = [
    path('blog', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', cat_blog_list, name='blog_list_cat'),
    path('blog/<slug:slugcat>/<slug:slugblog>/', blog_detail, name='blog_detail'),
]
