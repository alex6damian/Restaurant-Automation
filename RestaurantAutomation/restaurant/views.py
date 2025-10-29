from django.shortcuts import render

# Create your views here.

def home(request):
    
    context = {
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)

def menu(request):
    context = {
        'page_title': 'Menu',
    }
    return render(request, 'menu.html', context)