<?php
require "config.php";
require "libs/ibsng_api.php";
require "libs/bot_functions.php";

$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

// دریافت تنظیمات هشدار
$warning_limit = $conn->query("SELECT value FROM settings WHERE name = 'warning_limit'")->fetch_assoc()['value'];

// بررسی مصرف کاربران
$users = $conn->query("SELECT users.telegram_id, accounts.data_used 
                       FROM accounts 
                       JOIN users ON accounts.user_id = users.id");

while ($user = $users->fetch_assoc()) {
    if ($user['data_used'] >= $warning_limit) {
        file_get_contents("https://api.telegram.org/bot{$config['bot_token']}/sendMessage?chat_id={$user['telegram_id']}&text=" . urlencode("⚠️ هشدار مصرف! شما به حد مجاز مصرف خود نزدیک شده‌اید. لطفاً اکانت خود را تمدید کنید."));
    }
}

// بررسی اکانت‌های منقضی‌شده
$conn->query("UPDATE accounts SET status='expired' WHERE expiry_date < NOW()");
$config = require "config.php";
$ibsng = new IBSngAPI($config['ibsng_url'], $config['ibsng_user'], $config['ibsng_pass']);

// دریافت لیست تمام کاربران
$users = getAllUsers(); 

foreach ($users as $user) {
    $info = $ibsng->getAccountInfo($user['chat_id']);
    
    if ($info['credit'] < 1) { // اگر حجم کمتر از 1 گیگ باشد
        sendMessage($user['chat_id'], "⚠️ هشدار! حجم اینترنت شما کم است. لطفاً تمدید کنید.");
    }
}


?>
