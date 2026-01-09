from django.shortcuts import render

# Create your views here.

def credits(request):
    return render(request, 'credits/credits.html')
