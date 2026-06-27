from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from destinations.models import Destination
from .models import Booking


@login_required
def create_booking(request, destination_id):

    destination = get_object_or_404(
        Destination,
        id=destination_id
    )

    if request.method == 'POST':

        start_date = request.POST.get(
            'start_date'
        )

        people = int(
            request.POST.get(
                'people',
                1
            )
        )

        Booking.objects.create(
            user=request.user,
            destination=destination,
            start_date=start_date,
            people=people,
            total_price=destination.price * people
        )

        messages.success(
            request,
            'Đặt chuyến thành công.'
        )

        return redirect(
            'bookings:booking_history'
        )

    return redirect(
        'destinations:destination_list'
    )


@login_required
def booking_history(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'bookings/booking_history.html',
        {
            'bookings': bookings
        }
    )