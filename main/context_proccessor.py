from .models import News

def latest_news(request):
    latest_news = News.query.order_by(-"created_at")[:10]

    context = {
        "latest_news": latest_news
    }
    return context
