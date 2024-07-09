from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import admin
from .models import Blog, MetaData, Category
from .views import import_csv
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    list_filter = ('parent',)
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}

class MetaDataInline(admin.TabularInline):
    model = MetaData
    extra = 1

class BlogAdmin(admin.ModelAdmin):
    autocomplete_fields = ['categories']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'author', 'publish_date', 'is_published')
    search_fields = ('title', 'content', 'author')
    list_filter = ('is_published', 'publish_date')
    inlines = [MetaDataInline]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_button'] = True
        return super().changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(import_csv), name='import_csv'),
        ]
        return custom_urls + urls

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category,CategoryAdmin)