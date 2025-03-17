<?php
require "../config.php";
session_start();

if ($_SESSION['admin'] !== true) {
    die("⛔ شما دسترسی به این بخش ندارید.");
}

$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

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
