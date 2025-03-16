#!/bin/bash

set -e  # متوقف کردن اسکریپت در صورت خطا

echo "🚀 شروع نصب Novingate Bot..."

# 1️⃣ بروزرسانی سیستم و نصب پکیج‌های مورد نیاز
echo "📦 در حال بروزرسانی سیستم و نصب ابزارهای ضروری..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv mysql-server certbot unzip nano curl ufw

# 2️⃣ تنظیم دسترسی‌های لازم
echo "🔑 تنظیم مجوزهای روت..."
sudo chmod -R 777 /root

# 3️⃣ ایجاد دایرکتوری پروژه
echo "📁 ایجاد دایرکتوری پروژه..."
sudo mkdir -p /opt/novingate-bot
sudo chmod -R 777 /opt/novingate-bot

# 4️⃣ دریافت سورس کد از گیت‌هاب
echo "📥 کلون کردن مخزن گیت‌هاب..."
cd /opt/novingate-bot
sudo git clone https://github.com/milad-fe1/novingate-bot.git .
sudo chmod -R 777 /opt/novingate-bot

# 5️⃣ نصب وابستگی‌های پایتون
echo "🐍 نصب وابستگی‌های پایتون..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6️⃣ دریافت اطلاعات نصب از کاربر
echo "🔧 لطفاً اطلاعات نصب را وارد کنید:"

read -p "📌 دامنه ربات (مثال: bot.example.com): " DOMAIN
read -p "🤖 توکن ربات: " BOT_TOKEN
read -p "🆔 آیدی عددی ادمین: " ADMIN_ID
read -p "🛢️ نام دیتابیس: " DB_NAME
read -p "👤 نام کاربری دیتابیس: " DB_USER
read -sp "🔑 رمز عبور دیتابیس: " DB_PASS
echo
read -p "📧 ایمیل برای دریافت SSL: " SSL_EMAIL

# 7️⃣ ایجاد فایل `.env`
echo "📄 ایجاد فایل تنظیمات `.env`..."
cat <<EOF > .env
BOT_TOKEN=$BOT_TOKEN
ADMIN_ID=$ADMIN_ID
DB_HOST=localhost
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASS=$DB_PASS
DOMAIN=$DOMAIN
SSL_EMAIL=$SSL_EMAIL
EOF

# 8️⃣ تنظیم SSL و وبهوک
echo "🔐 دریافت گواهی SSL از Let's Encrypt..."
sudo certbot certonly --standalone -d $DOMAIN --email $SSL_EMAIL --agree-tos --non-interactive
echo "0 0 1 * * certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null

echo "🌐 تنظیم وبهوک تلگرام..."
WEBHOOK_URL="https://$DOMAIN"
curl -F "url=$WEBHOOK_URL" "https://api.telegram.org/bot$BOT_TOKEN/setWebhook"

# 9️⃣ تنظیم فایروال
echo "🛡️ تنظیم فایروال برای امنیت بیشتر..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# 🔟 ایجاد دیتابیس و جداول
echo "🛢️ ایجاد دیتابیس و جداول..."
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
sudo mysql -u root -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
sudo mysql -u root -e "FLUSH PRIVILEGES;"
python3 setup_database.py

# 1️⃣1️⃣ تنظیم `systemd` برای اجرای دائمی
echo "⚙️ تنظیم سرویس Systemd برای اجرای دائمی ربات..."
cat <<EOF | sudo tee /etc/systemd/system/novingate.service
[Unit]
Description=Novingate Telegram Bot
After=network.target

[Service]
ExecStart=/opt/novingate-bot/venv/bin/python /opt/novingate-bot/bot.py
WorkingDirectory=/opt/novingate-bot
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable novingate
sudo systemctl start novingate

# 1️⃣2️⃣ نصب phpMyAdmin برای مدیریت دیتابیس
echo "🛠️ نصب phpMyAdmin..."
sudo apt install -y phpmyadmin
sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

# 1️⃣3️⃣ بررسی موفقیت نصب
echo "✅ بررسی موفقیت نصب..."
if systemctl is-active --quiet novingate; then
    echo "🎉 ربات با موفقیت نصب و اجرا شد!"
    echo "🌍 آدرس وبهوک: $WEBHOOK_URL"
    echo "🔐 phpMyAdmin: http://$DOMAIN/phpmyadmin"
    echo "ℹ️ اطلاعات دیتابیس:"
    echo "   🔹 نام دیتابیس: $DB_NAME"
    echo "   🔹 نام کاربری: $DB_USER"
    echo "   🔹 رمز عبور: $DB_PASS"
else
    echo "❌ خطا در اجرای ربات! لطفاً لاگ‌ها را بررسی کنید."
fi
