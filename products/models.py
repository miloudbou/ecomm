from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# نموذج التصنيف
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# نموذج المنتج
class Product(models.Model):
    title = models.CharField(max_length=255)  # عنوان المنتج
    description = models.TextField() 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default=1)  # ربط المنتج بالتصنيف (مع ID فئة افتراضي)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # السعر
    image_url = models.URLField(blank=True, null=True)  # رابط الصورة (صورة عبر الإنترنت)
    created_at = models.DateTimeField(default=now)  # تاريخ إنشاء المنتج

    def get_price_display(self):
        """إرجاع السعر مع العملة"""
        from django.conf import settings
        return f"{self.price} {settings.CURRENCY_SYMBOL}"

    def __str__(self):
        return self.title  # عرض عنوان المنتج

# نموذج السلة
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"سلة {self.user.username if self.user else 'مجهول'}"

# نموذج عنصر السلة
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} × {self.product.title}"

# نموذج الطلب
class Order(models.Model):
    PAYMENT_METHODS = [
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cod')
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    customer_phone = models.CharField(max_length=15)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} - {self.payment_method}"

# نموذج عنصر الطلب
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} × {self.product.title} في الطلب {self.order.id}"
