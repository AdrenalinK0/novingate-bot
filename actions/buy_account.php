<?php
require "../config.php";
require "../libs/ibsng_api.php";
require "../libs/bot_functions.php";

$config = require "../config.php";
$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);

$plan = "VIP"; // این مقدار باید از کاربر دریافت شود
$username = "user_" . rand(1000, 9999);
$password = rand(100000, 999999);
$credit = 10; // 10 گیگابایت اعتبار اولیه

$response = $ibsng->createAccount($username, $password, $plan, $credit);

if ($response['success']) {
    sendMessage($chat_id, "✅ **اکانت شما با موفقیت ساخته شد!**\n\n🔑 **نام کاربری:** `$username`\n🔒 **رمز عبور:** `$password`\n📊 **حجم:** `$credit GB`");
} else {
    sendMessage($chat_id, "⛔ خطا در ایجاد اکانت: " . $response['error']);
}
?>
