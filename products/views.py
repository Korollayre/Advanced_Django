from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from django.core.cache import cache

from products.models import ProductCategory, Product


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all().select_related()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all().select_related()


def get_products():
    if settings.LOW_CACHE:
        key = 'products_list'
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.all().select_related()
            cache.set(key, products_list)
        return products_list
    else:
        return Product.objects.all().select_related()


def get_products_by_category(pk):
    if settings.LOW_CACHE:
        key = f'products_by_category_pk{pk}'
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.filter(category_id=pk).select_related()
            cache.set(key, products_list)
        return products_list
    else:
        return Product.objects.filter(category_id=pk).select_related()


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {'title': 'GeekShop - Products',
               # 'categories': ProductCategory.objects.all().select_related(),
               'categories': get_links_menu(),
               }
    if category_id:
        # products = Product.objects.filter(category_id=category_id).select_related()
        products = get_products_by_category(category_id)
    else:
        # products = Product.objects.all().select_related()
        products = get_products()
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['products'] = products_paginator
    return render(request, 'products/products.html', context)
