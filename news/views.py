import feedparser

from django.shortcuts import render
from django.core.cache import cache


def news_list(request):

    articles = cache.get(
        'travel_news'
    )

    if articles is None:

        print("GỌI RSS TỪ NEW YORK TIMES")

        url = (
            'https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml'
        )

        feed = feedparser.parse(
            url
        )

        articles = feed.entries[:10]

        cache.set(
            'travel_news',
            articles,
            60 * 2
        )

    else:

        print("LẤY TIN TỨC TỪ CACHE")

    return render(
        request,
        'news/news_list.html',
        {
            'articles': articles
        }
    )

'''
def news_list(request):

    url = (
        'https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml'
    )

    feed = feedparser.parse(
        url
    )

    articles = feed.entries[:10]

    return render(
        request,
        'news/news_list.html',
        {
            'articles': articles
        }
    )
'''
