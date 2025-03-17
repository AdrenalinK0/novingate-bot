<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$text = $_POST['message']; // متن پیام از ورودی دریافت می‌شود
$users = getAllUsers();

foreach ($users as $user) {
    sendMessage($user['chat_id'], $text);
}

sendMessage($config['admin_id'], "✅ پیام به تمام کاربران ارسال شد!");
?>
