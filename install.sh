#!/bin/bash

set -e

echo "🚀 نصب ربات Novingate شروع شد..."

# به‌روزرسانی و نصب پکیج‌های ضروری
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip mysql-server nginx certbot python3-certbot-nginx

# ایجاد فولدر و دریافت سورس از GitHub
if [ ! -d "/opt/novingate-bot" ]; then
    sudo git clone https://github.com/milad-fe1/novingate-bot.git /opt/novingate-bot
fi
cd /opt/novingate-bot

# ایجاد محیط مجازی پایتون و نصب وابستگی‌ها
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# تنظیمات دیتابیس
echo "🔹 لطفاً اطلاعات دیتابیس را وارد کنید:"
read -p "👉 نام دیتابیس: " DB_NAME
read -p "👉 نام کاربری دیتابیس: " DB_USER
read -s -p "👉 رمز عبور دیتابیس: " DB_PASS
echo ""
read -p "👉 دامنه ربات (مثال: bot.example.com): " DOMAIN

# ایجاد دیتابیس و کاربر
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# ذخیره اطلاعات در فایل .env
cat > /opt/novingate-bot/.env <<EOL
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASS=$DB_PASS
DOMAIN=$DOMAIN
EOL

# اجرای اسکریپت دیتابیس
python3 setup_database.py

# تنظیم وب‌سرور Nginx
sudo bash -c "cat > /etc/nginx/sites-available/novingate <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF"

sudo ln -s /etc/nginx/sites-available/novingate /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# دریافت گواهی SSL
sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m youremail@example.com

# تنظیم اجرای دائمی با systemd
sudo bash -c "cat > /etc/systemd/system/novingate.service <<EOF
[Unit]
Description=Novingate Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/opt/novingate-bot
ExecStart=/opt/novingate-bot/venv/bin/python3 /opt/novingate-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

# فعال‌سازی سرویس
sudo systemctl daemon-reload
sudo systemctl enable novingate
sudo systemctl start novingate

echo "✅ نصب ربات Novingate با موفقیت انجام شد!"
