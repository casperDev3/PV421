# news/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsForm

from notifications.consumers import MassMailerConsumer


# 1. READ (List) - Список новин
def news_list(request):
    news = News.objects.all()
    smm = MassMailerConsumer()
    print("test1")
    smm.send_mass_mail_update(
        {
            "message": "Новини були переглянуті користувачем."
        }
    )
    print("test2")
    return render(request, 'news/news_list.html', {'news': news})

# 1. READ (Detail) - Деталі однієї новини
def news_detail(request, pk):
    item = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'item': item})

# 2. CREATE - Створення новини
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Створити'})

# 3. UPDATE - Редагування
def news_edit(request, pk):
    item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=item.pk)
    else:
        form = NewsForm(instance=item)
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Редагувати'})

# 4. DELETE - Видалення
def news_delete(request, pk):
    item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'item': item})