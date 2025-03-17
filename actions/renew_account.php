<?php
require "../config.php";
require "../libs/ibsng_api.php";
require "../libs/bot_functions.php";

$config = require "../config.php";
$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);

$username = "user_1234"; // باید از دیتابیس دریافت شود
$extra_credit = 5; // 5 گیگابایت تمدید

$response = $ibsng->updateCredit($username, $extra_credit);

if ($response['success']) {
    sendMessage($chat_id, "✅ اکانت شما با **{$extra_credit}GB** تمدید شد!");
} else {
    sendMessage($chat_id, "⛔ خطا در تمدید اکانت: " . $response['error']);
}
?>
