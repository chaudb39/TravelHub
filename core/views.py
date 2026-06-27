from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

import time

#cache
from django.core.cache import cache
from destinations.models import Destination

def home(request):
    theme = request.COOKIES.get('theme', 'light')

    featured_destinations = cache.get(
        'featured_destinations'
    )

    if featured_destinations is None:

        print("QUERY DATABASE LẤY ĐỊA ĐIỂM NỔI BẬT")

        featured_destinations = Destination.objects.filter(
            is_featured=True
        ).order_by(
            '-created_at'
        )[:6]

        cache.set(
            'featured_destinations',
            featured_destinations,
            60 * 2
        )

    else:
        print("LẤY DỮ LIỆU TỪ CACHE")

    services = [
        {
            'title': 'Lịch trình thông minh',
            'description': 'Gợi ý lịch trình du lịch phù hợp với thời gian và sở thích của bạn.',
            'image': 'images/service1.png'
        },
        {
            'title': 'Địa điểm nổi bật',
            'description': 'Khám phá những điểm đến đẹp, nổi tiếng và đáng trải nghiệm.',
            'image': 'images/service2.png'
        },
        {
            'title': 'Trải nghiệm cá nhân',
            'description': 'Lưu lại sở thích, lựa chọn theme và cá nhân hóa trải nghiệm.',
            'image': 'images/service3.png'
        },
    ]

    return render(
        request,
        'core/home.html',
        {
            'theme': theme,
            'services': services,
            'featured_destinations': featured_destinations,
        }
    )

'''
def home(request):
    theme = request.COOKIES.get('theme', 'light')

    services = [
        {
            'title': 'Lịch trình thông minh',
            'description': 'Gợi ý lịch trình du lịch phù hợp với thời gian và sở thích của bạn.',
            'image': 'images/service1.png'
        },
        {
            'title': 'Địa điểm nổi bật',
            'description': 'Khám phá những điểm đến đẹp, nổi tiếng và đáng trải nghiệm.',
            'image': 'images/service2.png'
        },
        {
            'title': 'Trải nghiệm cá nhân',
            'description': 'Lưu lại sở thích, lựa chọn theme và cá nhân hóa trải nghiệm.',
            'image': 'images/service3.png'
        },
    ]

    return render(request, 'core/home.html', {
        'theme': theme,
        'services': services,
    })
'''

'''
def about(request):
    theme = request.COOKIES.get('theme', 'light')

    return render(request, 'core/about.html', {
        'theme': theme
    })
'''
def about(request):

    print("Đang render About Page...")

    time.sleep(5)

    return render(
        request,
        'core/about.html'
    )

def contact(request):
    theme = request.COOKIES.get('theme', 'light')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"""
Người gửi: {name}
Email: {email}

Nội dung:
{message}
"""

        send_mail(
            subject=f'[TravelHub] {subject}',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                settings.CONTACT_RECEIVER_EMAIL
            ],
            fail_silently=False
        )

        messages.success(
            request,
            'Gửi liên hệ thành công.'
        )

        return redirect('core:contact')

    return render(request, 'core/contact.html', {
        'theme': theme
    })


def set_theme(request, theme):
    response = redirect(request.META.get('HTTP_REFERER', '/'))

    if theme in ['light', 'dark']:
        response.set_cookie(
            'theme',
            theme,
            max_age=7 * 24 * 60 * 60
        )

    return response