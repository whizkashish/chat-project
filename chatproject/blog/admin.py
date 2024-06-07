from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import admin
from .models import Blog, MetaData, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ['name']

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

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category,CategoryAdmin)