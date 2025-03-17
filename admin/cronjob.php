<?php
require "../config.php";
session_start();

if ($_SESSION['admin'] !== true) {
    die("⛔ شما دسترسی به این بخش ندارید.");
}

$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

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
