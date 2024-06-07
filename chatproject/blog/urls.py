# urls.py

from django.urls import path
from .views import blog_list, blog_detail, import_csv
from core.views import CategoryAutocomplete
urlpatterns = [
    path('import-csv/', import_csv, name='import_csv'),
    path('blogs', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
]
