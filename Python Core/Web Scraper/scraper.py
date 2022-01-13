import requests
import string
import os
from bs4 import BeautifulSoup

URL = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='


def rename(name: str):
    result = name[:]
    for i in string.punctuation:
        result = result.replace(i, '')
    result = '_'.join(result.split())
    return result + '.txt'


def save_articles(num, articles_type):
    """Saves topics from num pages"""
    for i in range(1, num + 1):
        save_page_articles(URL, i, articles_type)


def save_page_articles(url, page_num, articles_type):
    """Saves topics from one pages"""
    os.mkdir(f'Page_{page_num}')
    url += str(page_num)
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=articles_type)

    found_articles = []
    for news_article in news_article_links:
        found_articles.append(news_article.find_parent('article').find('a', {'data-track-action': 'view article'}))

    for article in found_articles:
        file_name = rename(article.text)
        with open(fr'Page_{page_num}\{file_name}', 'w', encoding='utf-8') as f:
            url = 'https://www.nature.com' + article['href']
            r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(r.content, 'html.parser')
            news_text = soup.find('div', 'c-article-body u-clearfix')
            news_text = news_text.findChildren(['p', 'h2'])

            for div in news_text:
                f.write(div.text.strip())


if __name__ == '__main__':
    num_pages = int(input())
    type_of_topics = input()
    save_articles(num_pages, type_of_topics)
    print('Saved all articles.')
