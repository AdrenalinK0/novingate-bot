<?php
require "config.php";

$update = json_decode(file_get_contents("php://input"), true);
$chat_id = $update["message"]["chat"]["id"];
$text = $update["message"]["text"];
$user_id = $update["message"]["from"]["id"];

// اتصال به دیتابیس
$conn = new mysqli($config['db_host'], $config['db_user'], $config['db_pass'], $config['db_name']);

// بررسی اینکه کاربر ثبت‌نام شده است یا خیر
$user_check = $conn->query("SELECT * FROM users WHERE telegram_id = '$user_id'");
if ($user_check->num_rows == 0) {
    $conn->query("INSERT INTO users (telegram_id, balance) VALUES ('$user_id', 0)");
}

// توابع ارسال پیام
function sendMessage($chat_id, $text, $keyboard = null) {
    $data = [
        "chat_id" => $chat_id,
        "text" => $text,
        "parse_mode" => "HTML",
    ];
    if ($keyboard) {
        $data["reply_markup"] = json_encode(["keyboard" => $keyboard, "resize_keyboard" => true]);
    }
    file_get_contents("https://api.telegram.org/bot{$GLOBALS['config']['bot_token']}/sendMessage?" . http_build_query($data));
}

// دکمه‌های اصلی
$main_menu = [
    [["text" => "🛒 خرید اکانت"], ["text" => "📂 اکانت‌های من"]],
    [["text" => "💰 کیف پول"], ["text" => "🎫 پشتیبانی"]],
    [["text" => "📚 آموزش‌ها"], ["text" => "📢 زیرمجموعه‌گیری"]],
];

// پردازش دستورات کاربران
if ($text == "/start") {
    sendMessage($chat_id, "👋 خوش آمدید! لطفاً از منوی زیر گزینه مورد نظر را انتخاب کنید:", $main_menu);
} elseif ($text == "🛒 خرید اکانت") {
    $plans = $conn->query("SELECT * FROM plans");
    $plan_buttons = [];
    while ($plan = $plans->fetch_assoc()) {
        $plan_buttons[] = [["text" => "💳 {$plan['name']} - {$plan['price']} تومان"]];
    }
    sendMessage($chat_id, "لطفاً یکی از پلن‌های زیر را انتخاب کنید:", $plan_buttons);
} elseif ($text == "📂 اکانت‌های من") {
    $accounts = $conn->query("SELECT * FROM accounts WHERE user_id = (SELECT id FROM users WHERE telegram_id = '$user_id')");
    $message = "📂 اکانت‌های شما:\n";
    while ($acc = $accounts->fetch_assoc()) {
        $message .= "🔹 <b>نام کاربری:</b> {$acc['username']}\n";
        $message .= "📅 <b>تاریخ انقضا:</b> {$acc['expiry_date']}\n";
        $message .= "----------------------\n";
    }
    sendMessage($chat_id, $message);
} elseif ($text == "💰 کیف پول") {
    $balance = $conn->query("SELECT balance FROM users WHERE telegram_id = '$user_id'")->fetch_assoc()['balance'];
    sendMessage($chat_id, "💰 موجودی شما: <b>{$balance}</b> تومان\nبرای افزایش موجودی روی دکمه زیر کلیک کنید.", [
        [["text" => "➕ افزایش موجودی"]],
    ]);
} elseif ($text == "➕ افزایش موجودی") {
    sendMessage($chat_id, "🔢 لطفاً مبلغ شارژ را به تومان وارد کنید (حداقل 30000 تومان):");
} elseif (is_numeric($text) && $text >= 30000) {
    $conn->query("UPDATE users SET pending_amount = '$text' WHERE telegram_id = '$user_id'");
    sendMessage($chat_id, "✅ مبلغ انتخابی شما: $text تومان\nلطفاً روش پرداخت را انتخاب کنید:", [
        [["text" => "💳 درگاه بانکی"], ["text" => "🏦 کارت به کارت"]],
    ]);
} elseif ($text == "🏦 کارت به کارت") {
    $admin_card = $conn->query("SELECT value FROM settings WHERE name = 'admin_card'")->fetch_assoc()['value'];
    sendMessage($chat_id, "🔹 لطفاً مبلغ را به شماره کارت زیر واریز کنید:\n💳 <b>$admin_card</b>\nسپس رسید پرداخت خود را ارسال کنید.");
} elseif (!empty($update["message"]["photo"])) {
    $file_id = end($update["message"]["photo"])["file_id"];
    $conn->query("UPDATE users SET last_receipt = '$file_id' WHERE telegram_id = '$user_id'");
    sendMessage($chat_id, "📤 رسید شما دریافت شد. پس از تأیید، کیف پول شما شارژ خواهد شد.");
} elseif ($text == "🎫 پشتیبانی") {
    sendMessage($chat_id, "✏️ لطفاً سوال خود را ارسال کنید:");
} elseif (!empty($text) && $text != "/start") {
    $conn->query("INSERT INTO tickets (user_id, message) VALUES ((SELECT id FROM users WHERE telegram_id = '$user_id'), '$text')");
    sendMessage($chat_id, "📨 پیام شما دریافت شد. تیم پشتیبانی به زودی پاسخ خواهد داد.");
}

if ($data == "manage_accounts") {
    $keyboard = [
        [
            ["text" => "📌 مشاهده اکانت‌های من", "callback_data" => "my_accounts"],
            ["text" => "➕ خرید اکانت جدید", "callback_data" => "buy_account"]
        ],
        [
            ["text" => "🔄 تمدید اکانت", "callback_data" => "renew_account"],
            ["text" => "📊 وضعیت مصرف", "callback_data" => "usage_status"]
        ],
        [["text" => "🔙 بازگشت", "callback_data" => "main_menu"]]
    ];
    sendMessage($chat_id, "📢 لطفاً گزینه مورد نظر را انتخاب کنید:", $keyboard);
}

?>
