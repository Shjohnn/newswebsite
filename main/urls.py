from django.urls import path
from . import views


urlpatterns = [
    path('news/',views.index,name='index'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),

]