from django.urls import path

from newsletters.apps import NewslettersConfig
from newsletters.views import index

app_name = NewslettersConfig.name

urlpatterns = [
   path('', index, name='newsletters')
]