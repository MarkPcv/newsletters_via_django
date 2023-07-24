from django.contrib import admin

from newsletters.models import Client, Content, Newsletter, Trial


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'fullname',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'settings', 'title', 'message',)
    search_fields = ('title', 'message',)


@admin.register(Trial)
class TrialAdmin(admin.ModelAdmin):
    list_display = ('date', 'status',)
    ordering = ('date',)
    list_filter = ('content',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'time', 'frequency', 'status')
    list_filter = ('status', 'frequency')