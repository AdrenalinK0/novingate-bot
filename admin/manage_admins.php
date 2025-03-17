<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$admins = getAllAdmins();

$message = "🛠 **لیست ادمین‌ها:**\n\n";
foreach ($admins as $admin) {
    $message .= "👤 **آیدی:** {$admin['chat_id']}\n";
    $message .= "📌 **دسترسی:** {$admin['role']}\n";
    $message .= "———————————\n";
}
sendMessage($config['admin_id'], $message);
?>
