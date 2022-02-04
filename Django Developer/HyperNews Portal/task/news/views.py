import json
import random
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect


NEWS_PATH = r"hypernews\news.json"


def home_url(request):
    return redirect('/news/')


def article(request, news_id):
    with open(NEWS_PATH, "r") as json_file:
        news_dict = dict()
        for i in json.load(json_file):
            news_dict[i['link']] = i
    return render(request, 'news/article.html', context=news_dict[news_id])


def main_page(request):
    q = request.GET.get('q')  # Take data from searching form
    with open(NEWS_PATH, "r") as json_file:
        news_list = sorted(json.load(json_file),
                           key=lambda art: datetime.strptime(art["created"], '%Y-%m-%d %H:%M:%S'),
                           reverse=True)
        grouped_news = []
        for news in news_list:
            for group in grouped_news:
                if not q:  # if search form is empty
                    if group['date'] == news['created'][:10]:
                        group['news'].append(news)
                        break
                else:
                    if group['date'] == news['created'][:10] and q in news['title']:
                        group['news'].append(news)
                        break
            else:
                if not q or q in news['title']:
                    grouped_news.append({'date': news['created'][:10], 'news': [news]})
    return render(request, 'news/news_list.html', context={'news_list': grouped_news})


def create_news(request):
    if request.method == 'POST':
        with open(NEWS_PATH, "r") as json_file:
            news_list = json.load(json_file)
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text = request.POST.get('text')
            title = request.POST.get('title')
            while True:
                link = random.randint(0, 10000)
                for news in news_list:
                    if news['link'] == link:
                        break
                else:
                    break
        news_list.append({'created': created, 'text': text, 'title': title, 'link': link})
        with open(NEWS_PATH, "w", encoding="utf-8") as file:
            json.dump(news_list, file)
        return redirect('/news/')
    return render(request, 'news/create_news.html')
