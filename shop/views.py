from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Wishlist
from .forms import ReviewForm


def product_list(request, category_slug=None):
    """Главная страница со списком товаров и фильтрацией"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Фильтрация по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фильтр по цене (используем price или discount_price)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Применяем фильтр по цене с учетом скидки
    if min_price:
        try:
            min_price = float(min_price)
            # Товары где цена со скидкой >= min_price ИЛИ обычная цена >= min_price
            products = products.filter(
                Q(price__gte=min_price) | Q(discount_price__gte=min_price)
            )
        except ValueError:
            min_price = None

    if max_price:
        try:
            max_price = float(max_price)
            # Товары где цена со скидкой <= max_price ИЛИ обычная цена <= max_price
            products = products.filter(
                Q(price__lte=max_price) | Q(discount_price__lte=max_price)
            )
        except ValueError:
            max_price = None

    # Получаем минимальную и максимальную цену для слайдера
    all_products = Product.objects.filter(available=True)
    if category_slug:
        all_products = all_products.filter(category=category)

    # Вычисляем min и max цены (учитывая скидку)
    price_min = 0
    price_max = 10000

    for product in all_products:
        current_price = product.discount_price if product.discount_price else product.price
        if current_price < price_min or price_min == 0:
            price_min = float(current_price)
        if current_price > price_max:
            price_max = float(current_price)

    # Пагинация
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
        'min_price': min_price if min_price else price_min,
        'max_price': max_price if max_price else price_max,
        'price_min_global': int(price_min),
        'price_max_global': int(price_max),
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    """Страница конкретного товара с отзывами"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # Похожие товары
    similar_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    # Обработка отзыва
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('shop:product_detail', id=product.id, slug=product.slug)
    else:
        form = ReviewForm()

    # Получаем все отзывы
    reviews = product.reviews.all()

    # Вычисляем средний рейтинг
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
        avg_rating = round(avg_rating, 1)
    else:
        avg_rating = 0

    context = {
        'product': product,
        'similar_products': similar_products,
        'reviews': reviews,
        'form': form,
        'avg_rating': avg_rating,
        'reviews_count': reviews.count(),
    }
    return render(request, 'shop/product/detail.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """Добавить товар в избранное"""
    product = get_object_or_404(Product, id=product_id, available=True)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f'Товар "{product.name}" добавлен в избранное!')
    else:
        messages.info(request, f'Товар "{product.name}" уже в избранном')

    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


@login_required
def remove_from_wishlist(request, product_id):
    """Удалить товар из избранного"""
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'Товар "{product.name}" удален из избранного')
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


@login_required
def wishlist_detail(request):
    """Страница избранного"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/wishlist/detail.html', {'wishlist_items': wishlist_items})