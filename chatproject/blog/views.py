# views.py
import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import BlogImportForm
from .models import Blog, MetaData, Category
from django.utils.text import slugify

def blog_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 10)  # Show 10 blogs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/archive.html', {'page_obj': page_obj})


def cat_blog_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    blogs = Blog.objects.filter(is_published=True,categories=category).all()
    paginator = Paginator(blogs, 12)  # Show 10 blogs per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/cat-list.html', {'page_obj': page_obj,'category':category})

def blog_detail(request, slugcat, slugblog):
    category = get_object_or_404(Category, slug=slugcat)
    blog = get_object_or_404(Blog, slug=slugblog)
     # Fetch the previous blog based on the primary key
    previous_blog = Blog.objects.filter(id__lt=blog.id, categories=category.id).order_by('-id').first()
    
    # Fetch the next blog based on the primary key
    next_blog = Blog.objects.filter(id__gt=blog.id, categories=category.id).order_by('id').first()
    
    context = {
        'category': category,
        'blog': blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
    }
    return render(request, 'blog/single.html', context)
@staff_member_required
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
                category, _ = Category.objects.get_or_create(title=category_name,slug=slugify(category_name))
                blog, created = Blog.objects.update_or_create(
                    title=title,
                    defaults={
                        'content': content,
                        'slug': slug,
                        'is_published': is_published,
                        'categories_id': 1
                    }
                )
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
