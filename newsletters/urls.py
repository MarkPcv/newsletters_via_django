from django.urls import path

from newsletters.apps import NewslettersConfig
from newsletters.views import index, ClientListView, ClientCreateView

app_name = NewslettersConfig.name

urlpatterns = [
   path('', ClientListView.as_view(), name='client_list'),
   path('client/create', ClientCreateView.as_view(), name='client_create'),
]