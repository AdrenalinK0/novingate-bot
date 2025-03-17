<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$chat_id = $_POST['chat_id']; // آی‌دی ادمین جدید از ورودی
$role = "support"; // سطح دسترسی

if (addAdmin($chat_id, $role)) {
    sendMessage($chat_id, "✅ شما به عنوان **ادمین** منصوب شدید!");
} else {
    sendMessage($config['admin_id'], "⛔ خطا در افزودن ادمین!");
}
?>
