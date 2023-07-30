from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_published', 'title', 'content', 'views_count')
    search_fields = ('title', 'content',)
    ordering = ('date_published',)
