import json
import os

# تحديد المسار الصحيح للملف
products_file = os.path.join(os.getcwd(), 'products', 'ebay_products.json')

# فتح وتحميل البيانات من ebay_products.json
with open(products_file, 'r', encoding='utf-8') as file:
    products = json.load(file)

# تنظيف البيانات (تصحيح الأسعار مثلاً)
for product in products:
    # تنظيف السعر (إزالة أي نص إضافي أو تصحيح الفاصلة)
    price = product['price'].replace(' EUR', '').replace('$', '').replace(',', '.').strip()
    product['price'] = price

# حفظ البيانات النظيفة في ملف جديد
cleaned_file = os.path.join(os.getcwd(), 'products', 'cleaned_ebay_products.json')
with open(cleaned_file, 'w', encoding='utf-8') as file:
    json.dump(products, file, ensure_ascii=False, indent=4)

print("✅ تم تنظيف البيانات وتحديثها وحفظها في cleaned_ebay_products.json")

