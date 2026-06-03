# Імпортуємо необхідні функції для рендерингу шаблонів, обробки помилок 404 та перенаправлень
from django.shortcuts import render, get_object_or_404, redirect
# Імпортуємо декоратор для обмеження доступу неавторизованим користувачам
from django.contrib.auth.decorators import login_required
# Імпортуємо моделі бази даних з поточного додатку
from .models import Product, Category, Order, OrderItem


def product_list(request):
    """Відображає список товарів із можливістю фільтрації за категоріями."""

    # Отримуємо ID категорії з GET-параметрів URL (наприклад, ?category=2)
    category_id = request.GET.get('category')

    # Якщо параметр категорії присутній, фільтруємо товари за цією категорією
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    # Якщо категорії немає, отримуємо абсолютно всі товари з бази даних
    else:
        products = Product.objects.all()

    # Отримуємо всі категорії (зазвичай для відображення меню фільтрів на сторінці)
    categories = Category.objects.all()

    # Рендеримо HTML-шаблон та передаємо йому словник з даними (контекст)
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_id
    })


def product_detail(request, pk):
    """Відображає детальну інформацію про конкретний товар."""

    # Шукаємо товар за його первинним ключем (Primary Key - pk).
    # Якщо товар не знайдено, автоматично повертаємо сторінку з помилкою 404.
    product = get_object_or_404(Product, pk=pk)

    # Відображаємо шаблон деталей товару та передаємо знайдений об'єкт
    return render(request, 'shop/product_detail.html', {'product': product})


# Декоратор вимагає, щоб користувач був авторизований.
# Якщо ні — його перенаправлять на '/admin/login/'
@login_required(login_url='/admin/login/')
def buy_now(request, pk):
    """Обробляє швидку покупку одного товару ('Купити зараз')."""

    # Знаходимо товар, який користувач хоче придбати (або повертаємо 404 помилку)
    product = get_object_or_404(Product, pk=pk)

    # Створюємо нове замовлення у базі даних, прив'язуючи його до поточного користувача
    order = Order.objects.create(
        customer=request.user,  # Замовник - поточний авторизований користувач
        status='New',  # Початковий статус замовлення
        total=product.price  # Загальна сума дорівнює ціні одного товару
    )

    # Створюємо запис про конкретний товар у цьому замовленні
    OrderItem.objects.create(
        order=order,  # Прив'язуємо до щойно створеного замовлення
        product=product,  # Вказуємо куплений товар
        quantity=1,  # Кількість за замовчуванням - 1 шт.
        price=product.price  # Фіксуємо ціну товару на момент покупки
    )

    # Рендеримо сторінку успішного оформлення замовлення, передаючи інформацію про нього
    return render(request, 'shop/order_success.html', {'order': order})