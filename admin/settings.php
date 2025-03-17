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
// دریافت تنظیمات
$settings = [];
$result = $conn->query("SELECT * FROM settings");
while ($row = $result->fetch_assoc()) {
    $settings[$row['name']] = $row['value'];
}

// ذخیره تغییرات
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $admin_card = $_POST['admin_card'];
    $warning_limit = $_POST['warning_limit'];

    $conn->query("UPDATE settings SET value='$admin_card' WHERE name='admin_card'");
    $conn->query("UPDATE settings SET value='$warning_limit' WHERE name='warning_limit'");

    echo "✅ تنظیمات بروزرسانی شد!";
}

?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت تنظیمات</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>⚙️ مدیریت تنظیمات</h2>
    <form method="post">
        <label>💳 شماره کارت ادمین:</label>
        <input type="text" name="admin_card" value="<?= $settings['admin_card'] ?>" required>
        
        <label>🚨 هشدار مصرف (حجم مصرفی قبل از هشدار به کاربر بر حسب گیگ):</label>
        <input type="number" name="warning_limit" value="<?= $settings['warning_limit'] ?>" required>

        <button type="submit">💾 ذخیره تغییرات</button>
    </form>
</body>
</html>
