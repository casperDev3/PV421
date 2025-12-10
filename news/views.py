from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsForm

### CRUD - Create, Read, Update, Delete ###

# 1. Create News - Crud
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Створити'})


# 2. Read All News - cRud
def news_list(request):
    news_items = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news_items})


# 3. Read Single News - cRud
def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'item': news_item})


# 4. Update News - crUd
def news_edit(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news_item.pk)
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Редагувати'})


# 5. Delete News - cruD
def news_delete(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news_item.delete()
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'item': news_item})
