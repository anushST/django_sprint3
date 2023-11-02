from django.db.models.functions import Now
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def post_list_request():
    return Post.objects.select_related(
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
    )


def index(request: HttpRequest) -> HttpResponse:
    template_name: dict = 'blog/index.html'
    utc_now = Now()
    post_list = post_list_request().filter(
        pub_date__lte=utc_now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]  # тут я не понял что надо изменить
    context: dict = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    template_name: str = 'blog/detail.html'
    utc_now = Now()
    post = get_object_or_404(
        post_list_request().filter(
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
        # Мне же не все объекты нужны, зачем мне всё вызывать
        Category,
        slug=category_slug
    )

    if not category.is_published:
        raise Http404('Категория не опубликована')

    utc_now = Now()
    post_list = post_list_request().filter(
        pub_date__lte=utc_now,
        is_published=True,
        category__slug=category_slug
    )

    context: dict = {
        'post_list': post_list,
        'category': category
    }
    return render(request, template_name, context)
