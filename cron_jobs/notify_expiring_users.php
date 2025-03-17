<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$expiring_users = getExpiringUsers();

foreach ($expiring_users as $user) {
    sendMessage($user['chat_id'], "⚠️ اشتراک شما در حال اتمام است! لطفاً برای تمدید اقدام کنید.");
}
?>
