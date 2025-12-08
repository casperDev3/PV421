from django.shortcuts import render

def wish_view(request):
    return render(request, 'index.html')


