from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post


def post_list(request):
    theme = request.COOKIES.get('theme', 'light')

    posts = Post.objects.filter(is_published=True).order_by('-created_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/post_list.html', {
        'theme': theme,
        'page_obj': page_obj
    })


def post_detail(request, pk):
    theme = request.COOKIES.get('theme', 'light')

    post = get_object_or_404(Post, pk=pk, is_published=True)

    return render(request, 'posts/post_detail.html', {
        'theme': theme,
        'post': post
    })
