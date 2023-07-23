from django.shortcuts import render
from django.views.generic import ListView

from newsletters.models import Client


def index(request):
    # Testing
    return render(request, 'newsletters/base.html')


class ClientListView(ListView):
    model = Client