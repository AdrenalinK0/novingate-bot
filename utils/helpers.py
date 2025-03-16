import re
from datetime import datetime, timedelta

def validate_email(email: str) -> bool:
    """
    بررسی معتبر بودن ایمیل.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """
    بررسی معتبر بودن شماره تلفن (فرض: شماره تلفن ایرانی).
    """
    pattern = r'^09\d{9}$'
    return re.match(pattern, phone) is not None

def generate_referral_code(user_id: int) -> str:
    """
    تولید کد معرف بر اساس آی‌دی کاربر.
    """
    return f"REF{user_id:06d}"

def calculate_expiration_date(days: int) -> str:
    """
    محاسبه تاریخ انقضا بر اساس تعداد روزهای داده شده.
    """
    expiration_date = datetime.now() + timedelta(days=days)
    return expiration_date.strftime("%Y-%m-%d")

def format_balance(balance: float) -> str:
    """
    فرمت‌دهی موجودی به صورت زیبا (با جداکننده هزارگان).
    """
    return f"{balance:,.2f} تومان"

def is_admin(user_id: int, admins: list) -> bool:
    """
    بررسی آیا کاربر ادمین است یا نه.
    """
    return user_id in admins

def sanitize_input(input_str: str) -> str:
    """
    پاک‌سازی ورودی کاربر از کاراکترهای خطرناک.
    """
    return input_str.strip().replace("'", "").replace('"', '')

def generate_random_password(length: int = 8) -> str:
    """
    تولید یک پسورد تصادفی با طول مشخص.
    """
    import random
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def format_date(date_str: str) -> str:
    """
    فرمت‌دهی تاریخ به شکل خوانا برای کاربر.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d %b %Y")