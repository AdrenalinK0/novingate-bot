<?php
require "../config.php";
session_start();

// بررسی دسترسی ادمین
if ($_SESSION['admin'] !== true) {
    die("⛔ شما دسترسی به این بخش ندارید.");
}

// اتصال به دیتابیس
$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);
if ($conn->connect_error) {
    die("❌ خطا در اتصال به دیتابیس: " . $conn->connect_error);
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
