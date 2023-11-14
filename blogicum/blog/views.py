from django.db.models.functions import Now
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .constants import POSTS_LIMIT
from .models import Category, Post


def post_list_request(manager=Post.objects):
    return manager.select_related(
        'location', 'author', 'category'
    ).only(
        'id',
        'title',
        'text',
        'pub_date',
        'location__is_published',
        'location__name',
        'author__username',
        'category__slug',
        'category__title'
    ).filter(
        pub_date__lte=Now(),
        is_published=True,
        category__is_published=True
    )


def index(request: HttpRequest) -> HttpResponse:
    template_name: dict = 'blog/index.html'
    post_list = post_list_request().order_by('-pub_date')[:POSTS_LIMIT]
    context: dict = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    template_name: str = 'blog/detail.html'
    post = get_object_or_404(
        post_list_request(),
        pk=post_id
    )
    context: dict = {
        'post': post,
    }
    return render(request, template_name, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    template_name: str = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = post_list_request(category.post_set)

    context: dict = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template_name, context)
