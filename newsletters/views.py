from django.shortcuts import render

def index(request):
    # Testing
    return render(request, 'newsletters/base.html')
