from rest_framework import serializers
from .models import Product  # تأكد من استيراد الـ Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # الآن سيتم التعرف على الـ Product
        fields = ['title', 'category', 'price']
