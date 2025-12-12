from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from .models import *
from django.db.models import Q

def index(request):
    new_news = News.objects.all().first()
    latest_news = News.objects.all().order_by('-published_at')[1:5]
    featuerd_news = News.objects.all().order_by('-published_at')[6:10]
    next=News.objects.all()[11:13]
    next1=News.objects.all()[14:17]
    next2=News.objects.all()[18:21]
    next3=News.objects.all()[21:22]
    most_read = News.objects.all().order_by('-views')[:5]



    context={
        'new_news':new_news,
        'latest_news':latest_news,
        'featuerd_news':featuerd_news,
        'next':next,
        'next1':next1,
        'next2':next2,
        'next3':next3,
        'most_read':most_read,


    }
    return render(request,'index.html',context)


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, is_published=True)
    news.views += 1
    news.save(update_fields=['views'])
    comments = Comment.objects.filter(
        news=news,
        is_approved=True
    ).order_by('-created_at')[:3]
    most_read = News.objects.all().order_by('-views')[:5]


    context={
        'news':news,
        'comments':comments,
        'most_read':most_read,
    }
    return render(request, 'single.html', context)


def contact(request):
    """
    Aloqa sahifasi
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Barcha maydonlar to'ldirilganligini tekshirish
        if name and email and subject and message:
            # Ma'lumotni saqlash
            from .models import ContactMessage
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.')
            return redirect('contact')
        else:
            messages.error(request, 'Barcha maydonlarni to\'ldiring!')

    return render(request, 'contact.html')


def add_comment(request, slug):
    """
    Izoh qo'shish
    """
    if request.method == 'POST':
        news = get_object_or_404(News, slug=slug, is_published=True)

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validatsiya
        if name and email and message:
            Comment.objects.create(
                news=news,
                name=name,
                email=email,
                message=message,
                is_approved=True  # Admin tasdiqlashi kerak
            )

            # Success xabari (messages framework'siz)
            from django.http import HttpResponseRedirect
            from django.urls import reverse

            # Yangilik sahifasiga qaytish
            return HttpResponseRedirect(
                reverse('news_detail', kwargs={'slug': news.slug}) + '?comment=success'
            )
        else:
            # Error bilan qaytish
            return HttpResponseRedirect(
                reverse('news_detail', kwargs={'slug': news.slug}) + '?comment=error'
            )

    # Agar GET request bo'lsa, yangilik sahifasiga yo'naltirish
    return redirect('home')


def search_view(request):
    query = request.GET.get('q')
    results=[]
    if query:
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    context = {
        'results':results,
        'query':query,
    }
    return render(request, 'search.html', context)