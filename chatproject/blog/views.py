# views.py
import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import BlogImportForm
from .models import Blog, MetaData, Category
from django.utils.text import slugify

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
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode('utf-8').splitlines()
            
            # Skip the header row
            reader = csv.DictReader(file_data)
            #next(reader)  # Skip the header row
            
            for row in reader:
                title = row['title']
                content = row['content'].replace("\\n","\n").splitlines()
                text12 = content.pop(0)
                content = '<br>'.join(content)
                slug = slugify(title)
                is_published = True  # Assuming all imported blogs are published
                category_name = "The Understated Dominance"
                category, _ = Category.objects.get_or_create(name=category_name)
                blog, created = Blog.objects.update_or_create(
                    title=title,
                    defaults={
                        'content': content,
                        'slug': slug,
                        'is_published': is_published,
                    }
                )
                blog.categories.add(category)
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
    return render(request, 'admin/blog/import_blogs.html', {'csvform':form})
