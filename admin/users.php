<?php
require "../config.php";
require "../libs/ibsng_api.php";

$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);
$users = $ibsng->getActiveUsers();
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

// دریافت لیست کاربران
$users = $conn->query("SELECT * FROM users");

// مدیریت کاربر (افزایش/کاهش موجودی، مسدود کردن)
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user_id = $_POST['user_id'];

    if (isset($_POST['ban'])) {
        $conn->query("UPDATE users SET banned = 1 WHERE id = '$user_id'");
        echo "🚫 کاربر مسدود شد.";
    }

    if (isset($_POST['unban'])) {
        $conn->query("UPDATE users SET banned = 0 WHERE id = '$user_id'");
        echo "✅ کاربر رفع مسدود شد.";
    }

    if (isset($_POST['balance_change'])) {
        $amount = $_POST['balance_amount'];
        $conn->query("UPDATE users SET balance = balance + $amount WHERE id = '$user_id'");
        echo "💰 تغییر موجودی اعمال شد.";
    }
}
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت کاربران</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>👥 مدیریت کاربران</h2>
    <table border="1">
        <tr>
            <th>آیدی تلگرام</th>
            <th>موجودی</th>
            <th>عملیات</th>
        </tr>
        <?php while ($user = $users->fetch_assoc()): ?>
            <tr>
                <td><?= $user['telegram_id'] ?></td>
                <td><?= $user['balance'] ?> تومان</td>
                <td>
                    <form method="post">
                        <input type="hidden" name="user_id" value="<?= $user['id'] ?>">
                        <input type="number" name="balance_amount" placeholder="مبلغ تغییر" required>
                        <button type="submit" name="balance_change">💰 تغییر موجودی</button>
                        <?php if ($user['banned'] == 0): ?>
                            <button type="submit" name="ban">🚫 مسدود کردن</button>
                        <?php else: ?>
                            <button type="submit" name="unban">✅ رفع مسدودیت</button>
                        <?php endif; ?>
                    </form>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
    <h2>👥 کاربران فعال</h2>
    <table border="1">
        <tr>
            <th>نام کاربری</th>
            <th>حجم مصرفی</th>
            <th>اعتبار باقی‌مانده</th>
            <th>عملیات</th>
        </tr>
        <?php foreach ($users as $user): ?>
        <tr>
            <td><?= $user['user_id'] ?></td>
            <td><?= $user['usage'] ?> GB</td>
            <td><?= $user['credit'] ?> GB</td>
            <td>
                <a href="delete_user.php?username=<?= $user['user_id'] ?>">❌ حذف</a>
            </td>
        </tr>
        <?php endforeach; ?>
    </table>


</body>
</html>


