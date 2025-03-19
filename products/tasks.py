from celery import shared_task
from .fetch_products import fetch_products_from_website

@shared_task
def scheduled_fetch_products():
    try:
        data = fetch_products_from_website()  # استبدال some_function()
        print(f"🟢 Data received: {data}")

        if not data:  # تأكد أن البيانات ليست فارغة
            print("❌ لم يتم استلام أي بيانات!")
            return "❌ لم يتم استلام أي بيانات!"

        if not isinstance(data, (list, tuple)):  
            print(f"❌ البيانات غير صالحة (يجب أن تكون قائمة أو Tuple): {type(data)} - {data}")
            return "❌ البيانات المرجعة ليست قائمة أو Tuple!"

        if len(data) < 3:
            print(f"❌ البيانات غير كافية: {data}")
            return f"❌ البيانات غير كافية! يجب أن تكون 3 عناصر على الأقل، ولكن تم استلام {len(data)} عنصر فقط."

        # أخذ أول 3 قيم فقط إذا كانت القائمة تحتوي على أكثر من 3 عناصر
        var1, var2, var3 = data[:3]
        print(f"✅ Processed: {var1}, {var2}, {var3}")
        return f"✅ Processed: {var1}, {var2}, {var3}"

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
        return f"❌ حدث خطأ غير متوقع: {str(e)}"
