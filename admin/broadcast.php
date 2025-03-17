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
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $message = $_POST['message'];
    $users = $conn->query("SELECT telegram_id FROM users");
    while ($user = $users->fetch_assoc()) {
        file_get_contents("https://api.telegram.org/bot{$config['bot_token']}/sendMessage?chat_id={$user['telegram_id']}&text=" . urlencode($message));
    }
    echo "✅ پیام همگانی ارسال شد.";
}
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ارسال پیام همگانی</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>📢 ارسال پیام همگانی</h2>

    <form method="post">
        <textarea name="message" placeholder="متن پیام..." required></textarea>
        <button type="submit">📨 ارسال</button>
    </form>
</body>
</html>
