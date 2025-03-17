#!/bin/bash

# تنظیم رنگ‌ها برای نمایش پیام‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # بدون رنگ

echo -e "${CYAN}🚀 شروع فرآیند نصب ربات Novingate...${NC}"

# ** ۱) دریافت اطلاعات از کاربر **
read -p "🔹 دامنه ربات (با https://): " bot_domain
read -p "🔹 توکن ربات تلگرام: " bot_token
read -p "🔹 آی‌دی عددی ادمین: " admin_id
read -p "🔹 نام دیتابیس: " db_name
read -p "🔹 نام کاربری دیتابیس: " db_user
read -s -p "🔹 رمز عبور دیتابیس: " db_pass
echo

echo -e "${YELLOW}✅ اطلاعات دریافت شد. در حال نصب وابستگی‌ها...${NC}"

# ** ۲) بروزرسانی و نصب نرم‌افزارهای مورد نیاز **
echo -e "${CYAN}📦 نصب نرم‌افزارهای مورد نیاز (Apache, MySQL, PHP, Certbot, Composer, Curl)...${NC}"
apt update -y
apt install apache2 mysql-server php php-mbstring php-xml php-bcmath php-curl php-zip php-cli unzip certbot python3-certbot-nginx composer curl -y

echo -e "${GREEN}✅ نرم‌افزارهای مورد نیاز نصب شدند.${NC}"

# ** ۳) ایجاد دایرکتوری‌های مورد نیاز **
echo -e "${CYAN}📁 در حال ایجاد دایرکتوری‌های پروژه...${NC}"
mkdir -p /var/www/novingate-bot/{logs,config,src}
chmod -R 777 /var/www/novingate-bot
echo -e "${GREEN}✅ دایرکتوری‌های مورد نیاز ایجاد شدند.${NC}"

# ** ۴) تنظیم گواهی SSL **
echo -e "${CYAN}🔐 در حال صدور گواهی SSL برای دامنه...${NC}"
certbot --nginx -d "$bot_domain" --non-interactive --agree-tos -m admin@"$bot_domain"

# افزودن کرون‌جاب برای تمدید خودکار SSL
echo "0 0 */89 * * certbot renew --quiet" | crontab -
echo -e "${GREEN}✅ گواهی SSL صادر شد و تمدید خودکار تنظیم شد.${NC}"

# ** ۵) تنظیم MySQL و ایجاد دیتابیس و کاربر **
echo -e "${CYAN}📊 در حال تنظیم دیتابیس MySQL...${NC}"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS $db_name;"
mysql -u root -e "CREATE USER IF NOT EXISTS '$db_user'@'localhost' IDENTIFIED BY '$db_pass';"
mysql -u root -e "GRANT ALL PRIVILEGES ON $db_name.* TO '$db_user'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"

echo -e "${GREEN}✅ دیتابیس و کاربر MySQL تنظیم شدند.${NC}"

# ** ۶) ایجاد جداول دیتابیس **
echo -e "${CYAN}📊 در حال ایجاد جداول دیتابیس...${NC}"
mysql -u "$db_user" -p"$db_pass" "$db_name" < db.sql
echo -e "${GREEN}✅ جداول دیتابیس ایجاد شدند.${NC}"

# ** ۷) نصب phpMyAdmin **
echo -e "${CYAN}🛠 در حال نصب phpMyAdmin...${NC}"
apt install phpmyadmin -y
ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin
echo -e "${GREEN}✅ phpMyAdmin نصب شد.${NC}"

# ** ۸) تنظیم وبهوک ربات تلگرام **
echo -e "${CYAN}🔗 در حال تنظیم وبهوک...${NC}"
webhook_url="$bot_domain/webhook.php"
curl -X POST "https://api.telegram.org/bot$bot_token/setWebhook?url=$webhook_url"
echo -e "${GREEN}✅ وبهوک روی '$webhook_url' تنظیم شد.${NC}"

# ** ۹) ذخیره اطلاعات در `config.php` **
echo -e "${CYAN}📄 در حال ذخیره تنظیمات در فایل config.php...${NC}"
cat <<EOL > /var/www/novingate-bot/config.php
<?php
return [
    'bot_token' => '$bot_token',
    'admin_id' => '$admin_id',
    'db_host' => 'localhost',
    'db_name' => '$db_name',
    'db_user' => '$db_user',
    'db_pass' => '$db_pass',
    'bot_domain' => '$bot_domain'
];
EOL
echo -e "${GREEN}✅ تنظیمات ذخیره شد.${NC}"

# ** ۱۰) اجرای ربات و تنظیم کرون‌جاب برای اجرا مداوم **
echo -e "${CYAN}🚀 در حال اجرای ربات...${NC}"
nohup php /var/www/novingate-bot/bot.php > /var/www/novingate-bot/logs/bot.log 2>&1 &

# افزودن کرون‌جاب برای اجرا مداوم ربات
echo "* * * * * php /var/www/novingate-bot/bot.php > /dev/null 2>&1" | crontab -
echo -e "${GREEN}✅ ربات راه‌اندازی شد و در حال اجرا است.${NC}"

# ** ۱۱) نمایش اطلاعات به کاربر **
echo -e "${GREEN}🎉 نصب با موفقیت انجام شد!${NC}"
echo -e "${CYAN}🔗 phpMyAdmin: http://$bot_domain/phpmyadmin${NC}"
echo -e "${CYAN}📊 دیتابیس: $db_name${NC}"
echo -e "${CYAN}👤 نام کاربری: $db_user${NC}"
echo -e "${CYAN}🔑 رمز عبور: $db_pass${NC}"
echo -e "${CYAN}📌 وبهوک تنظیم شده: $webhook_url${NC}"

# ** ۱۲) ارسال پیام خوشامدگویی در تلگرام **
welcome_message="🎉 به ربات novingate خوش آمدید! 🚀\n✅ نصب با موفقیت انجام شد."
curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" -d "chat_id=$admin_id&text=$welcome_message"

exit 0
