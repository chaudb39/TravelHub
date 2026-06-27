from django.shortcuts import render, redirect
from destinations.models import Destination


def add_favorite(request, destination_id):
    favorites = request.session.get('favorites', [])

    if destination_id not in favorites:
        favorites.append(destination_id)

    request.session['favorites'] = favorites

    return redirect('destinations:destination_list')


def remove_favorite(request, destination_id):
    favorites = request.session.get('favorites', [])

    if destination_id in favorites:
        favorites.remove(destination_id)

    request.session['favorites'] = favorites

    return redirect('favorites:favorite_list')


def clear_favorites(request):
    request.session['favorites'] = []

    return redirect('favorites:favorite_list')


def favorite_list(request):
    theme = request.COOKIES.get('theme', 'light')

    favorite_ids = request.session.get('favorites', [])

    destinations = Destination.objects.filter(id__in=favorite_ids)

    return render(request, 'favorites/favorite_list.html', {
        'theme': theme,
        'destinations': destinations,
    })
