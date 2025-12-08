from django.shortcuts import render
from .models import Wish

def wish_view(request):
    wishes = Wish.objects.all()
    return render(request, 'index.html', {
        'test': 'Hello, World!',
        'wishes': wishes
    })


