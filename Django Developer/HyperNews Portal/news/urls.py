from django.urls import path
from news.views import home_url, article, main_page, create_news

urlpatterns = [
    path('', home_url),
    path('news/<int:news_id>/', article),
    path('news/', main_page),
    path('news/create/', create_news)
]
