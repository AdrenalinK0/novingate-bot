<?php
require "../config.php";
require "../libs/ibsng_api.php";
require "../libs/bot_functions.php";

$config = require "../config.php";
$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);

$accounts = $ibsng->getAccountInfo($chat_id); // چک کردن حساب کاربر

if (!$accounts) {
    sendMessage($chat_id, "⛔ شما هیچ اکانت فعالی ندارید.");
    exit;
}

$message = "📋 **لیست اکانت‌های شما:**\n\n";
foreach ($accounts as $acc) {
    $message .= "👤 **نام کاربری:** {$acc['user_id']}\n";
    $message .= "📅 **تاریخ انقضا:** {$acc['expire_date']}\n";
    $message .= "📊 **حجم باقی‌مانده:** {$acc['credit']} GB\n";
    $message .= "🔗 **اتصال:** {$acc['status']}\n";
    $message .= "———————————\n";
}

sendMessage($chat_id, $message);
?>
