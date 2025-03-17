<?php
require "../config.php";

$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

// دریافت تنظیمات کرون‌جاب
$settings = $conn->query("SELECT * FROM settings WHERE id = 1")->fetch_assoc();
$days_before_expire = $settings['days_before_expire'];
$traffic_limit = $settings['traffic_limit'];

// بررسی اکانت‌هایی که رو به انقضا هستند
$expiring_accounts = $conn->query("SELECT * FROM accounts WHERE expiry_date <= DATE_ADD(CURDATE(), INTERVAL $days_before_expire DAY)");

while ($account = $expiring_accounts->fetch_assoc()) {
    $user_id = $account['user_id'];
    $telegram_id = $conn->query("SELECT telegram_id FROM users WHERE id = $user_id")->fetch_assoc()['telegram_id'];
    
    $message = "⚠️ هشدار تمدید اکانت: اکانت شما در " . $account['expiry_date'] . " منقضی خواهد شد. لطفاً تمدید کنید.";
    file_get_contents("https://api.telegram.org/bot{$config['bot_token']}/sendMessage?chat_id={$telegram_id}&text=" . urlencode($message));
}

// بررسی میزان مصرف کاربران
$heavy_users = $conn->query("SELECT * FROM accounts WHERE data_used >= $traffic_limit * 1024 * 1024 * 1024");

while ($account = $heavy_users->fetch_assoc()) {
    $user_id = $account['user_id'];
    $telegram_id = $conn->query("SELECT telegram_id FROM users WHERE id = $user_id")->fetch_assoc()['telegram_id'];

    $message = "⚠️ هشدار مصرف: شما بیش از " . $traffic_limit . " گیگابایت از ترافیک خود را استفاده کرده‌اید.";
    file_get_contents("https://api.telegram.org/bot{$config['bot_token']}/sendMessage?chat_id={$telegram_id}&text=" . urlencode($message));
}

echo "✅ کرون‌جاب اجرا شد و پیام‌های هشدار ارسال شدند.";
?>
