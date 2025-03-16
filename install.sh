#!/bin/bash

# دریافت اطلاعات از کاربر به‌صورت مرحله‌به‌مرحله
echo "لطفاً اطلاعات مورد نیاز را وارد کنید:"
read -p "توکن ربات خود را وارد کنید: " TOKEN
read -p "نام کاربری MySQL را وارد کنید: " MYSQL_USER
read -p "رمز عبور MySQL را وارد کنید: " MYSQL_PASS
read -p "نام دیتابیس را وارد کنید: " MYSQL_DB
read -p "نام دامنه خود را وارد کنید (مثال: bot.example.com): " DOMAIN
read -p "آی‌دی عددی ادمین را وارد کنید: " ADMIN_ID

# ایجاد دایرکتوری‌های مورد نیاز
echo "بررسی و ایجاد دایرکتوری‌های مورد نیاز..."
mkdir -p database utils logs

# نصب وابستگی‌های سیستم
echo "نصب وابستگی‌های سیستم..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip mysql-server nginx

# تنظیم MySQL
echo "تنظیم MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DB};"
sudo mysql -e "CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASS}';"
sudo mysql -e "GRANT ALL PRIVILEGES ON ${MYSQL_DB}.* TO '${MYSQL_USER}'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# ایجاد فایل تنظیمات
echo "TOKEN = \"$TOKEN\"" > config.py
echo "MYSQL_CONFIG = {" >> config.py
echo "    \"host\": \"localhost\"," >> config.py
echo "    \"user\": \"$MYSQL_USER\"," >> config.py
echo "    \"password\": \"$MYSQL_PASS\"," >> config.py
echo "    \"database\": \"$MYSQL_DB\"" >> config.py
echo "}" >> config.py
echo "ADMIN_ID = $ADMIN_ID" >> config.py

# نصب وابستگی‌های پایتون
echo "نصب وابستگی‌های پایتون..."
pip3 install -r requirements.txt

# ایجاد جدول‌های مورد نیاز در دیتابیس
echo "ایجاد جدول‌های مورد نیاز در دیتابیس..."
mysql -u ${MYSQL_USER} -p${MYSQL_PASS} ${MYSQL_DB} < database/create_tables.sql

# نصب phpMyAdmin
echo "نصب phpMyAdmin..."
sudo apt-get install -y phpmyadmin

# تنظیم Nginx برای phpMyAdmin
echo "تنظیم Nginx برای phpMyAdmin..."
sudo bash -c "cat > /etc/nginx/sites-available/pma.${DOMAIN} <<EOF
server {
    listen 80;
    server_name pma.${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

sudo ln -s /etc/nginx/sites-available/pma.${DOMAIN} /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# تنظیم Nginx برای ربات
echo "تنظیم Nginx برای ربات..."
sudo bash -c "cat > /etc/nginx/sites-available/${DOMAIN} <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

sudo ln -s /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# ارسال پیام به ادمین
echo "ارسال پیام به ادمین..."
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
    -d "chat_id=${ADMIN_ID}" \
    -d "text=ربات با موفقیت نصب شد! 🎉\n\nنام دامنه: ${DOMAIN}\nphpMyAdmin: http://pma.${DOMAIN}\nتوکن ربات: ${TOKEN}"

# اجرای خودکار ربات
echo "اجرای خودکار ربات..."
nohup python3 bot.py > logs/bot.log 2>&1 &

# نمایش اطلاعات نصب
echo "✅ نصب با موفقیت انجام شد!"
echo "================================================"
echo "🔗 لینک دسترسی به ربات: http://${DOMAIN}"
echo "🔗 لینک دسترسی به phpMyAdmin: http://pma.${DOMAIN}"
echo "🔑 توکن ربات: ${TOKEN}"
echo "👤 آی‌دی ادمین: ${ADMIN_ID}"
echo "📂 دایرکتوری لاگ‌ها: $(pwd)/logs/bot.log"
echo "================================================"
echo "برای مشاهده لاگ‌های ربات، از دستور زیر استفاده کنید:"
echo "tail -f logs/bot.log"
echo "برای متوقف کردن ربات، از دستور زیر استفاده کنید:"
echo "pkill -f bot.py"
echo "================================================"