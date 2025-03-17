<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$chat_id = $_POST['chat_id'];

if (banUser($chat_id)) {
    sendMessage($chat_id, "⛔ حساب شما به دلیل تخلف مسدود شده است.");
    sendMessage($config['admin_id'], "✅ کاربر **$chat_id** مسدود شد.");
} else {
    sendMessage($config['admin_id'], "⛔ خطا در مسدودسازی کاربر!");
}
?>
