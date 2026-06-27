from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Avg

from .models import Destination
from reviews.forms import ReviewForm

#cache
from django.views.decorators.cache import cache_page

#per-view
@cache_page(60 * 2)  # cache trang này trong 2 phút
def destination_list(request):
    theme = request.COOKIES.get('theme', 'light')

    keyword = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    print("ĐANG QUERY DATABASE TRANG DESTINATIONS")

    destinations = Destination.objects.all().order_by('-created_at')

    if keyword:
        destinations = destinations.filter(
            name__icontains=keyword
        )

    if min_price:
        destinations = destinations.filter(
            price__gte=min_price
        )

    if max_price:
        destinations = destinations.filter(
            price__lte=max_price
        )

    paginator = Paginator(destinations, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'destinations/destination_list.html',
        {
            'theme': theme,
            'page_obj': page_obj,
            'keyword': keyword,
            'min_price': min_price,
            'max_price': max_price,
        }
    )

'''
def destination_list(request):
    theme = request.COOKIES.get('theme', 'light')

    keyword = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    destinations = Destination.objects.all().order_by('-created_at')

    if keyword:
        destinations = destinations.filter(
            name__icontains=keyword
        )

    if min_price:
        destinations = destinations.filter(
            price__gte=min_price
        )

    if max_price:
        destinations = destinations.filter(
            price__lte=max_price
        )

    paginator = Paginator(destinations, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'destinations/destination_list.html',
        {
            'theme': theme,
            'page_obj': page_obj,
            'keyword': keyword,
            'min_price': min_price,
            'max_price': max_price,
        }
    )
'''
def destination_detail(request, pk):
    theme = request.COOKIES.get('theme', 'light')

    destination = get_object_or_404(
        Destination,
        pk=pk
    )

    reviews = destination.reviews.select_related(
        'user'
    ).order_by(
        '-created_at'
    )

    average_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    review_form = ReviewForm()

    return render(
        request,
        'destinations/destination_detail.html',
        {
            'theme': theme,
            'destination': destination,
            'reviews': reviews,
            'average_rating': average_rating,
            'review_form': review_form,
        }
    )
    