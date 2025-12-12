from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.index, name='index'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_view, name='search'),

]
