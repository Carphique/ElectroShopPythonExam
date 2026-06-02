from django.db import models
from django.contrib.auth.models import User  # Вбудована модель користувача замість AppUser з C#


# 1. Аналог Category.cs
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")

    def __str__(self):
        return self.name


# 2. Аналог Product.cs (та ProductSpecs)
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.IntegerField(verbose_name="Кількість на складі")
    currency = models.CharField(max_length=10, default="UAH", verbose_name="Валюта")

    # Зв'язок з категорією
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категорія")

    # Зображення (замість FileStorage сервісу в C#, Django робить це автоматично)
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Зображення")

    created_at = models.DateTimeField(auto_now_add=True)

    # Характеристики (ProductSpecs.cs з C#). Для простоти додамо їх прямо сюди
    cpu = models.CharField(max_length=100, null=True, blank=True, verbose_name="Процесор")
    ram = models.CharField(max_length=100, null=True, blank=True, verbose_name="ОЗП")
    storage = models.CharField(max_length=100, null=True, blank=True, verbose_name="Пам'ять")

    def __str__(self):
        return f"{self.brand} {self.name}"


# 3. Аналог Order.cs
class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'Нове'),
        ('Processing', 'В обробці'),
        ('Completed', 'Виконано'),
    ]

    # Зв'язок з покупцем
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупець")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Загальна сума")

    def __str__(self):
        return f"Замовлення #{self.id} від {self.customer.username}"


# 4. Аналог OrderItem.cs
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна за одиницю")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"