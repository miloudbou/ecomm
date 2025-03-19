from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
import paypalrestsdk
from .models import Product, Order, OrderItem, Category
from .forms import OrderForm
from .serializers import ProductSerializer
from rest_framework import viewsets
from django.core.mail import send_mail
from django.contrib import messages
import logging

# إعداد السجل (Logging)
logger = logging.getLogger(__name__)

# تكوين PayPal عند بدء تشغيل التطبيق
paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET,
})

# عرض API للمنتجات
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# عرض قائمة المنتجات مع إمكانية البحث والتصفية حسب الفئة
def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')

    if search_query:
        products = products.filter(title__icontains=search_query)

    if category_id.isdigit():  # تأكد أن category_id رقم وليس نص
        products = products.filter(category__id=int(category_id))

    return render(request, 'products/product_list.html', {
        'products': products,
        'search': search_query,
        'category': category_id
    })

# عرض صفحة الدفع
def payment_page(request):
    return render(request, 'products/payment.html')

# إنشاء الدفع عبر PayPal
def create_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', '100')
        currency = request.POST.get('currency', settings.DEFAULT_CURRENCY)

        if currency == "DZD":
            try:
                amount = float(amount) * settings.EXCHANGE_RATE_DZD_TO_USD
                amount = round(amount, 2)
            except ValueError:
                return JsonResponse({'error': 'قيمة المبلغ غير صحيحة'}, status=400)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/execute/'),
                "cancel_url": request.build_absolute_uri('/payment/cancel/')
            },
            "transactions": [{
                "amount": {"total": str(amount), "currency": "USD"},
                "description": "الدفع مقابل المنتجات"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            logger.error("فشل إنشاء الدفع: %s", payment.error)
            return JsonResponse({'error': 'فشل في إنشاء الدفع', 'details': payment.error}, status=400)
    
    return render(request, 'products/payment.html')

# تنفيذ الدفع بعد موافقة المستخدم
def execute_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            messages.success(request, "✅ تم الدفع بنجاح!")
            return redirect('payment_success')
        else:
            messages.error(request, "❌ فشل الدفع!")
            return redirect('payment_failed')

    except Exception as e:
        logger.error(f"خطأ أثناء تنفيذ الدفع: {e}")
        messages.error(request, "حدث خطأ أثناء معالجة الدفع!")
        return redirect('payment_failed')
def payment_success(request):
    return render(request, "products/payment_success.html")
   

# عرض سلة التسوق
@login_required
def view_cart(request):
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    cart_items = order.items.all()
    
    # حساب الإجمالي لكل عنصر في السلة
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    # حساب المجموع الكلي للسلة
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# إضافة منتج إلى سلة التسوق
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
    if not item_created:
        order_item.quantity += 1
    order_item.save()
    return JsonResponse({"success": True, "message": "تمت الإضافة بنجاح!"})

# تحديث كمية المنتج في السلة
@login_required
def update_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        order = Order.objects.get(user=request.user, is_paid=False)
        order_item = get_object_or_404(OrderItem, order=order, product_id=product_id)
        order_item.quantity = quantity
        order_item.save()
    return redirect("view_cart")

# حذف منتج من السلة
@login_required
def remove_from_cart(request, product_id):
    order = Order.objects.get(user=request.user, is_paid=False)
    order.items.filter(product_id=product_id).delete()
    return redirect("view_cart")

# إنشاء طلب
@login_required
def create_order(request):
    try:
        order = Order.objects.get(user=request.user, is_paid=False)
        if order.items.exists():
            order.is_paid = True
            order.save()
            return redirect("order_success")
    except Order.DoesNotExist:
        messages.error(request, "❌ لم يتم العثور على الطلب!")
    
    return redirect("view_cart")

# صفحة نجاح الطلب
def order_success(request):
    return render(request, "products/order_success.html")

# عرض التصنيفات
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

# عرض المنتجات ضمن تصنيف معين
def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_products.html', {'category': category, 'products': products})

# الصفحة الرئيسية
def index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

# عرض تفاصيل المنتج
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/single.html', {'product': product})

# عرض صفحة الاتصال
def contact(request):
    return render(request, 'products/contact.html')

# صفحة فشل الدفع
def payment_failed(request):
    return render(request, "products/payment_failed.html")
