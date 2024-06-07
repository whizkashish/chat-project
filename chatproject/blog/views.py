# views.py
import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import BlogImportForm
from .models import Blog, MetaData

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)
    return render(request, 'blog/archive.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/single.html', {'blog': blog})

def import_csv(request):
    if request.method == 'POST':
        form = BlogImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                blog, created = Blog.objects.update_or_create(
                    title=row['title'],
                    defaults={
                        'content': row['content'],
                        'author': row['author'],
                        'slug': row['slug'],
                        'is_published': row['is_published'].lower() == 'true',
                    }
                )
                blog.save()
                # Handle metadata if present in CSV
                for key, value in row.items():
                    if key not in ['title', 'content', 'author', 'slug', 'is_published']:
                        MetaData.objects.update_or_create(
                            blog=blog,
                            key=key,
                            defaults={'value': value}
                        )

            messages.success(request, 'Blogs imported successfully.')
            return redirect('admin:blog_blog_changelist')
    else:
        form = BlogImportForm()
    return render(request, 'admin/blog/import_blogs.html')
