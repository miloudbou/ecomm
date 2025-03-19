import sqlite3
import json
import re  # استيراد مكتبة التعبيرات النمطية لمعالجة الأسعار

# إنشاء قاعدة البيانات والاتصال بها
conn = sqlite3.connect('database/ecommerce.db')  # تحديث المسار لقاعدة البيانات
cursor = conn.cursor()

# إنشاء جدول المنتجات
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price TEXT NOT NULL,
    image_url TEXT NOT NULL
)
''')

# تحميل المنتجات من JSON
with open('database/cleaned_ebay_products.json', 'r', encoding='utf-8') as file:  # تحديث المسار لملف JSON
    products = json.load(file)

# دالة لتنظيف الأسعار وإزالة النصوص غير المرغوب فيها
def clean_price(price):
    price = price.replace("EUR", "").strip()  # إزالة "EUR"
    price = re.sub(r'\s*à\s*', ' - ', price)  # استبدال "à" بـ "-"
    return price

# إدخال المنتجات في قاعدة البيانات مع تصحيح الأسعار
for product in products:
    cleaned_price = clean_price(product['price'])  # تنظيف السعر
    cursor.execute('''
    INSERT INTO products (title, price, image_url)
    VALUES (?, ?, ?)
    ''', (product['title'], cleaned_price, product['image_url']))

# حفظ التغييرات وإغلاق الاتصال
conn.commit()
conn.close()

print("✅ تم تخزين المنتجات في قاعدة البيانات بنجاح مع تصحيح الأسعار!")


