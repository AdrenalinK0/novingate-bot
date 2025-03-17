<?php
require "../config.php";
session_start();

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
// تنظیم کرون‌جاب
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $days_before_expire = $_POST['days_before_expire'];
    $traffic_limit = $_POST['traffic_limit'];
    
    $conn->query("UPDATE settings SET days_before_expire = $days_before_expire, traffic_limit = $traffic_limit WHERE id = 1");
    echo "✅ تنظیمات هشدار تمدید ذخیره شد.";
}

// دریافت تنظیمات
$settings = $conn->query("SELECT * FROM settings WHERE id = 1")->fetch_assoc();
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت کرون‌جاب</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>⏳ تنظیم هشدار تمدید اکانت</h2>

    <form method="post">
        <label>⏰ چند روز قبل از انقضا هشدار داده شود؟</label>
        <input type="number" name="days_before_expire" value="<?= $settings['days_before_expire'] ?>" required>

        <label>📊 حجم مصرفی که هشدار داده شود (GB)</label>
        <input type="number" name="traffic_limit" value="<?= $settings['traffic_limit'] ?>" required>

        <button type="submit">💾 ذخیره تنظیمات</button>
    </form>
</body>
</html>
