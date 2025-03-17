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

// افزودن پلن جدید
if ($_SERVER["REQUEST_METHOD"] == "POST" && $_POST['action'] == "add") {
    $name = $_POST['name'];
    $users = $_POST['users'];
    $days = $_POST['days'];
    $price = $_POST['price'];
    $conn->query("INSERT INTO plans (name, users, days, price) VALUES ('$name', $users, $days, $price)");
    header("Location: plans.php");
}

// حذف پلن
if (isset($_GET['delete'])) {
    $plan_id = $_GET['delete'];
    $conn->query("DELETE FROM plans WHERE id = $plan_id");
    header("Location: plans.php");
}

$plans = $conn->query("SELECT * FROM plans");
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت پلن‌های فروش</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>🛒 مدیریت پلن‌های فروش</h2>

    <form method="post">
        <input type="hidden" name="action" value="add">
        <input type="text" name="name" placeholder="نام پلن" required>
        <input type="number" name="users" placeholder="تعداد کاربران مجاز" required>
        <input type="number" name="days" placeholder="مدت زمان (روز)" required>
        <input type="number" name="price" placeholder="قیمت (تومان)" required>
        <button type="submit">➕ اضافه کردن</button>
    </form>

    <table>
        <tr>
            <th>نام پلن</th>
            <th>کاربران</th>
            <th>روزها</th>
            <th>قیمت</th>
            <th>عملیات</th>
        </tr>
        <?php while ($plan = $plans->fetch_assoc()): ?>
            <tr>
                <td><?= $plan['name'] ?></td>
                <td><?= $plan['users'] ?></td>
                <td><?= $plan['days'] ?></td>
                <td><?= number_format($plan['price']) ?> تومان</td>
                <td>
                    <a href="?delete=<?= $plan['id'] ?>">🗑 حذف</a>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>
