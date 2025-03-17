<?php
require "../config.php";
session_start();

// بررسی دسترسی ادمین
if ($_SESSION['admin'] !== true) {
    die("⛔ شما دسترسی به این بخش ندارید.");
}

// بررسی تعریف ثابت‌های دیتابیس
if (!defined('DB_HOST') || !defined('DB_USER') || !defined('DB_PASS') || !defined('DB_NAME')) {
    die("❌ ثابت‌های دیتابیس (DB_HOST, DB_USER, DB_PASS, DB_NAME) به درستی تعریف نشده‌اند!");
}

// ایجاد اتصال به دیتابیس
$mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

// بررسی موفقیت اتصال
if ($mysqli->connect_error) {
    die("❌ اتصال به دیتابیس ناموفق: " . $mysqli->connect_error);
} else {
    echo "✅ اتصال به دیتابیس موفقیت‌آمیز بود!<br>";
}

// تنظیم کاراکتر ست به utf8mb4 برای پشتیبانی از زبان فارسی
if (!$mysqli->set_charset("utf8mb4")) {
    echo "❌ خطا در تنظیم کاراکتر ست: " . $mysqli->error . "<br>";
}

// دریافت اطلاعات کلی
$total_users = $conn->query("SELECT COUNT(*) FROM users")->fetch_row()[0];
$total_wallet = $conn->query("SELECT SUM(wallet) FROM users")->fetch_row()[0] ?? 0;
$total_accounts = $conn->query("SELECT COUNT(*) FROM accounts")->fetch_row()[0];

?>
<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پنل مدیریت NovinGate</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>🎛 داشبورد مدیریت</h2>
    <p>👥 تعداد کل کاربران: <b><?= $total_users ?></b></p>
    <p>💰 مجموع موجودی کیف پول‌ها: <b><?= number_format($total_wallet) ?> تومان</b></p>
    <p>🔐 تعداد کل اکانت‌های فعال: <b><?= $total_accounts ?></b></p>

    <div class="buttons">
        <a href="users.php">👤 مدیریت کاربران</a>
        <a href="servers.php">🔧 مدیریت سرورها</a>
        <a href="payments.php">💳 مدیریت درگاه‌ها</a>
        <a href="tickets.php">📨 پشتیبانی</a>
    </div>
</body>
</html>
