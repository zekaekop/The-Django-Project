from django.shortcuts import render

# Create your views here.

def thanks(request):
    return render(request, "secret/thanks.html", {"test":15})