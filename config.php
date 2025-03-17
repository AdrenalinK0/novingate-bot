<?php

// جلوگیری از دسترسی مستقیم به فایل
if (!defined('APP_ACCESS')) {
    exit('Direct access to this file is not allowed.');
}

/**
 * فایل تنظیمات پروژه
 * مقادیر حساس باید در فایل .env تعریف شوند و از طریق متغیرهای محیطی لود شوند.
 * برای استفاده از این فایل، از composer require vlucas/phpdotenv نصب کنید.
 */

// لود کتابخانه phpdotenv برای مدیریت متغیرهای محیطی
if (file_exists(__DIR__ . '/vendor/autoload.php')) {
    require_once __DIR__ . '/vendor/autoload.php';
    $dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
    $dotenv->load();
} else {
    exit('❌ کتابخانه phpdotenv نصب نشده است. لطفاً دستور "composer require vlucas/phpdotenv" را اجرا کنید.');
}


return [
    // تنظیمات ربات تلگرام
    'bot_token' => getenv('BOT_TOKEN') ?: 'YOUR_BOT_TOKEN', // توکن ربات تلگرام
    'admin_id' => getenv('ADMIN_ID') ?: 'YOUR_ADMIN_ID',   // آیدی عددی ادمین

    // تنظیمات دیتابیس (بدون استفاده از ثابت‌ها)
    'db' => [
        'host' => getenv('DB_HOST') ?: '127.0.0.1',
        'user' => getenv('DB_USER') ?: 'your_database_username',
        'pass' => getenv('DB_PASS') ?: 'your_database_password',
        'name' => getenv('DB_NAME') ?: 'your_database_name',
    ],

    // تنظیمات IBSng
    'ibsng' => [
        'url' => getenv('IBSNG_URL') ?: 'https://ibsng.example.com',
        'user' => getenv('IBSNG_USER') ?: 'YOUR_IBSNG_ADMIN',
        'pass' => getenv('IBSNG_PASS') ?: 'YOUR_IBSNG_PASSWORD',
    ],

    // تنظیمات جوین اجباری
    'join' => [
        'required_channel' => getenv('REQUIRED_CHANNEL') ?: '@YourChannel',
        'required_group' => getenv('REQUIRED_GROUP') ?: '@YourGroup',
    ],
];

/**
 * تابع اعتبارسنجی تنظیمات
 * بررسی می‌کند که آیا مقادیر ضروری تنظیم شده‌اند یا خیر
 */
function validateConfig(array $config): void {
    $requiredKeys = ['bot_token', 'admin_id', 'db.host', 'db.user', 'db.pass', 'db.name'];
    foreach ($requiredKeys as $key) {
        $keys = explode('.', $key);
        $value = $config;
        foreach ($keys as $k) {
            $value = $value[$k] ?? null;
        }
        if (empty($value) || strpos($value, 'YOUR_') === 0) {
            exit("❌ مقدار '$key' در فایل تنظیمات به درستی تنظیم نشده است.");
        }
    }
}