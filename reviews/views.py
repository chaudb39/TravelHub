from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from destinations.models import Destination
from .forms import ReviewForm


@login_required
def add_review(request, destination_id):
    destination = get_object_or_404(
        Destination,
        id=destination_id
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()

            messages.success(
                request,
                'Đánh giá của bạn đã được gửi.'
            )

    return redirect(
        'destinations:destination_detail',
        pk=destination.id
    )
