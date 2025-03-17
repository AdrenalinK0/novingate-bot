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
    $server_address = $_POST['server_address'];
    $server_username = $_POST['server_username'];
    $server_password = $_POST['server_password'];
    $conn->query("INSERT INTO servers (address, username, password) VALUES ('$server_address', '$server_username', '$server_password')");
    header("Location: servers.php");
}

$servers = $conn->query("SELECT * FROM servers");

if (isset($_GET['delete'])) {
    $server_id = $_GET['delete'];
    $conn->query("DELETE FROM servers WHERE id = $server_id");
    header("Location: servers.php");
}
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت سرورها</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>🔧 مدیریت سرورها</h2>
    
    <form method="post">
        <input type="text" name="server_address" placeholder="آدرس سرور" required>
        <input type="text" name="server_username" placeholder="نام کاربری" required>
        <input type="password" name="server_password" placeholder="رمز عبور" required>
        <button type="submit">➕ اضافه کردن</button>
    </form>

    <table>
        <tr>
            <th>آدرس سرور</th>
            <th>نام کاربری</th>
            <th>عملیات</th>
        </tr>
        <?php while ($server = $servers->fetch_assoc()): ?>
            <tr>
                <td><?= $server['address'] ?></td>
                <td><?= $server['username'] ?></td>
                <td>
                    <a href="?delete=<?= $server['id'] ?>">🗑 حذف</a>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>
