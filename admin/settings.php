<?php
require "../config.php";
session_start();

if ($_SESSION['admin'] !== true) {
    die("⛔ شما دسترسی به این بخش ندارید.");
}

$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

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
