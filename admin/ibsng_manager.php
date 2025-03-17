<?php
require "../config.php";
require "../libs/ibsng_api.php";

$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);

// ایجاد کاربر جدید در IBSng
$username = "test_user";
$password = "123456";
$group_name = "VIP";
$credit = 10; // اعتبار به گیگابایت

$response = $ibsng->createAccount($username, $password, $group_name, $credit);

if ($response['success']) {
    echo "✅ اکانت کاربر با موفقیت ساخته شد!";
} else {
    echo "⛔ خطا در ایجاد اکانت: " . $response['error'];
}
?>
