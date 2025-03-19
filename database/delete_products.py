import sqlite3
import os

def delete_all_products():
    """حذف جميع المنتجات من قاعدة البيانات."""
    db_path = os.path.join(os.getcwd(), 'ecommerce.db')  # استخدام المسار المطلق
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # تنفيذ استعلام حذف جميع المنتجات من الجدول
        cursor.execute("DELETE FROM products")
        
        # حفظ التغييرات وإغلاق الاتصال
        conn.commit()
        conn.close()

        print("✅ تم حذف جميع المنتجات من قاعدة البيانات.")
    except sqlite3.Error as e:
        print(f"❌ حدث خطأ أثناء الاتصال بقاعدة البيانات: {e}")

if __name__ == "__main__":
    delete_all_products()
