from django.urls import path

from newsletters.apps import NewslettersConfig
from newsletters.views import ClientListView, ClientCreateView, \
   ClientDetailView, ClientUpdateView, ClientDeleteView, NewsletterListView, \
   NewsletterCreateView, NewsletterDetailView, NewsletterUpdateView, NewsletterDeleteView

app_name = NewslettersConfig.name

urlpatterns = [
   path('', ClientListView.as_view(), name='client_list'),
   path('client/create/', ClientCreateView.as_view(), name='client_create'),
   path('client/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
   path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
   path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
   path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
   path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
   path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_view'),
   path('newsletter/<int:pk>/update/', NewsletterUpdateView.as_view(), name='newsletter_update'),
   path('newsletter/<int:pk>/delete/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
]