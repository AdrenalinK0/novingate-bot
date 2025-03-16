import os
from dotenv import load_dotenv

# بارگیری متغیرهای محیطی از فایل .env
load_dotenv()

# اطلاعات ربات
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# اطلاعات دیتابیس
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# تنظیمات درگاه پرداخت
PAYMENT_GATEWAY = os.getenv("PAYMENT_GATEWAY")

# دامنه و SSL
DOMAIN = os.getenv("DOMAIN")
SSL_CERT_PATH = "/etc/letsencrypt/live/{}/fullchain.pem".format(DOMAIN)
SSL_KEY_PATH = "/etc/letsencrypt/live/{}/privkey.pem".format(DOMAIN)
