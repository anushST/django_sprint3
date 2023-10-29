from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from .models import Post, Category
import datetime


def index(request: HttpRequest) -> HttpResponse:
    template_name: dict = 'blog/index.html'
    utc_now = datetime.datetime.utcnow()
    post_list = Post.objects.select_related(
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
        pub_date__lte=utc_now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context: dict = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    template_name: str = 'blog/detail.html'
    utc_now = datetime.datetime.utcnow()
    post = get_object_or_404(
        Post.objects.select_related(
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
            pub_date__lte=utc_now,
            is_published=True,
            category__is_published=True
        ),
        pk=post_id
    )
    context: dict = {
        'post': post,
    }
    return render(request, template_name, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    template_name: str = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values(
            'title',
            'description',
            'is_published'
        ),
        slug=category_slug
    )

    if not category['is_published']:
        raise Http404('Категория не опубликована')

    utc_now = datetime.datetime.utcnow()
    post_list = Post.objects.select_related(
        'location', 'category', 'author'
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
        pub_date__lte=utc_now,
        is_published=True,
        category__slug=category_slug
    )

    context: dict = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template_name, context)
