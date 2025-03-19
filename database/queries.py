import sqlite3

# الاتصال بقاعدة البيانات
DB_PATH = "ecommerce.db"

def get_all_products():
    """ استرجاع جميع المنتجات من قاعدة البيانات """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, price, image_url FROM products")
    products = cursor.fetchall()

    conn.close()
    return products

def get_product_by_id(product_id):
    """ استرجاع منتج واحد حسب ID """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, price, image_url FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    conn.close()
    return product

def search_products(keyword):
    """ البحث عن المنتجات حسب الكلمة المفتاحية """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, price, image_url FROM products WHERE title LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()

    conn.close()
    return results

# **اختبار سريع عند تشغيل هذا الملف مباشرة**
if __name__ == "__main__":
    print("📦 جميع المنتجات:")
    for product in get_all_products():
        print(product)

    print("\n🔎 البحث عن 'Microsoft':")
    for product in search_products("Microsoft"):
        print(product)
