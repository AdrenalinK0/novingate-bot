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

// افزودن آموزش
if ($_SERVER["REQUEST_METHOD"] == "POST" && $_POST['action'] == "add") {
    $title = $_POST['title'];
    $content = $_POST['content'];
    $conn->query("INSERT INTO tutorials (title, content) VALUES ('$title', '$content')");
    header("Location: tutorials.php");
}

// حذف آموزش
if (isset($_GET['delete'])) {
    $tutorial_id = $_GET['delete'];
    $conn->query("DELETE FROM tutorials WHERE id = $tutorial_id");
    header("Location: tutorials.php");
}

$tutorials = $conn->query("SELECT * FROM tutorials");
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت آموزش‌ها</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>📚 مدیریت آموزش‌ها</h2>

    <form method="post">
        <input type="hidden" name="action" value="add">
        <input type="text" name="title" placeholder="عنوان آموزش" required>
        <textarea name="content" placeholder="متن آموزش" required></textarea>
        <button type="submit">➕ اضافه کردن</button>
    </form>

    <table>
        <tr>
            <th>عنوان</th>
            <th>محتوا</th>
            <th>عملیات</th>
        </tr>
        <?php while ($tutorial = $tutorials->fetch_assoc()): ?>
            <tr>
                <td><?= $tutorial['title'] ?></td>
                <td><?= $tutorial['content'] ?></td>
                <td>
                    <a href="?delete=<?= $tutorial['id'] ?>">🗑 حذف</a>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>
