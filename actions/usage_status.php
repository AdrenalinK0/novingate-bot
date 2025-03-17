<?php
require "../config.php";
require "../libs/ibsng_api.php";
require "../libs/bot_functions.php";

$config = require "../config.php";
$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);

$usage = $ibsng->getAccountInfo($chat_id);

if (!$usage) {
    sendMessage($chat_id, "⛔ اطلاعاتی برای شما یافت نشد.");
    exit;
}

$message = "📊 **وضعیت مصرف شما:**\n\n";
$message .= "📌 **حجم مصرف شده:** {$usage['usage']} GB\n";
$message .= "📉 **حجم باقی‌مانده:** {$usage['credit']} GB\n";
$message .= "🚀 **سرعت اتصال:** {$usage['speed']} Mbps\n";

sendMessage($chat_id, $message);
?>
