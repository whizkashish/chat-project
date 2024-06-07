from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete
from blog.models import Category

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Category.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
    
def index(request):
    return render(request, 'core/index.html')