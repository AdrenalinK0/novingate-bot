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

// دریافت تیکت‌های باز
$tickets = $conn->query("SELECT tickets.id, users.telegram_id, tickets.message 
                         FROM tickets 
                         JOIN users ON tickets.user_id = users.id 
                         WHERE tickets.status = 'open'");

// پاسخگویی به تیکت
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $ticket_id = $_POST['ticket_id'];
    $response = $_POST['response'];

    // دریافت اطلاعات کاربر
    $ticket = $conn->query("SELECT users.telegram_id 
                            FROM tickets 
                            JOIN users ON tickets.user_id = users.id 
                            WHERE tickets.id = '$ticket_id'")->fetch_assoc();

    $telegram_id = $ticket['telegram_id'];

    // ارسال پاسخ به کاربر
    file_get_contents("https://api.telegram.org/bot{$config['bot_token']}/sendMessage?chat_id={$telegram_id}&text=" . urlencode("📩 پاسخ پشتیبانی:\n$response"));

    // بستن تیکت
    $conn->query("UPDATE tickets SET status = 'closed' WHERE id = '$ticket_id'");
    echo "✅ پاسخ ارسال شد و تیکت بسته شد.";
}

?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت تیکت‌ها</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>🎫 مدیریت تیکت‌های پشتیبانی</h2>
    <table border="1">
        <tr>
            <th>آیدی تلگرام</th>
            <th>متن پیام</th>
            <th>پاسخ</th>
        </tr>
        <?php while ($ticket = $tickets->fetch_assoc()): ?>
            <tr>
                <td><?= $ticket['telegram_id'] ?></td>
                <td><?= $ticket['message'] ?></td>
                <td>
                    <form method="post">
                        <input type="hidden" name="ticket_id" value="<?= $ticket['id'] ?>">
                        <input type="text" name="response" placeholder="پاسخ خود را وارد کنید" required>
                        <button type="submit">📤 ارسال پاسخ</button>
                    </form>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>
