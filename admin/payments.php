<?php
require "../config.php";
session_start();

if ($_SESSION['admin'] !== true) {
    die("⛔ شما دسترسی به این بخش ندارید.");
}

$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if ($_POST['action'] == "add") {
        $type = $_POST['type'];
        $name = $_POST['name'];
        $api_key = $_POST['api_key'];
        $status = $_POST['status'];
        $conn->query("INSERT INTO payment_gateways (type, name, api_key, status) VALUES ('$type', '$name', '$api_key', '$status')");
    } elseif ($_POST['action'] == "toggle") {
        $id = $_POST['id'];
        $current_status = $_POST['current_status'];
        $new_status = $current_status == 1 ? 0 : 1;
        $conn->query("UPDATE payment_gateways SET status = $new_status WHERE id = $id");
    } elseif ($_POST['action'] == "delete") {
        $id = $_POST['id'];
        $conn->query("DELETE FROM payment_gateways WHERE id = $id");
    }
    header("Location: payments.php");
}

$gateways = $conn->query("SELECT * FROM payment_gateways");
?>

<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدیریت درگاه‌های پرداخت</title>
    <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
    <h2>💳 مدیریت درگاه‌های پرداخت</h2>
    
    <form method="post">
        <input type="hidden" name="action" value="add">
        <select name="type">
            <option value="rial">ریالی</option>
            <option value="crypto">ارزی (کریپتو)</option>
        </select>
        <input type="text" name="name" placeholder="نام درگاه" required>
        <input type="text" name="api_key" placeholder="API Key" required>
        <select name="status">
            <option value="1">فعال</option>
            <option value="0">غیرفعال</option>
        </select>
        <button type="submit">➕ اضافه کردن</button>
    </form>

    <table>
        <tr>
            <th>نوع</th>
            <th>نام درگاه</th>
            <th>API Key</th>
            <th>وضعیت</th>
            <th>عملیات</th>
        </tr>
        <?php while ($gateway = $gateways->fetch_assoc()): ?>
            <tr>
                <td><?= $gateway['type'] == 'rial' ? 'ریالی' : 'ارزی (کریپتو)' ?></td>
                <td><?= $gateway['name'] ?></td>
                <td><?= $gateway['api_key'] ?></td>
                <td><?= $gateway['status'] ? '✅ فعال' : '❌ غیرفعال' ?></td>
                <td>
                    <form method="post">
                        <input type="hidden" name="id" value="<?= $gateway['id'] ?>">
                        <input type="hidden" name="current_status" value="<?= $gateway['status'] ?>">
                        <button name="action" value="toggle">
                            <?= $gateway['status'] ? '🔴 غیرفعال' : '🟢 فعال کردن' ?>
                        </button>
                        <button name="action" value="delete">🗑 حذف</button>
                    </form>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>
