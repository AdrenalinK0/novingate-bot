<?php
require "../config.php";

// 📌 ارسال پیام به کاربر
function sendMessage($chat_id, $text, $markdown = false) {
    global $config;
    $bot_token = $config['bot_token'];
    $mode = $markdown ? "Markdown" : "HTML";

    $url = "https://api.telegram.org/bot$bot_token/sendMessage";
    $postData = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => $mode
    ];

    file_get_contents($url . "?" . http_build_query($postData));
}

// 📌 ارسال دکمه شیشه‌ای (Inline Keyboard)
function sendInlineKeyboard($chat_id, $text, $buttons) {
    global $config;
    $bot_token = $config['bot_token'];

    $url = "https://api.telegram.org/bot$bot_token/sendMessage";
    $postData = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => "HTML",
        'reply_markup' => json_encode(['inline_keyboard' => $buttons])
    ];

    file_get_contents($url . "?" . http_build_query($postData));
}

// 📌 بررسی اینکه آیا کاربر ثبت شده است یا نه
function userExists($chat_id) {
    global $pdo;
    $stmt = $pdo->prepare("SELECT * FROM users WHERE chat_id = ?");
    $stmt->execute([$chat_id]);
    return $stmt->rowCount() > 0;
}

// 📌 افزودن کاربر جدید به دیتابیس
function addUser($chat_id) {
    global $pdo;
    $stmt = $pdo->prepare("INSERT INTO users (chat_id, balance, joined_at) VALUES (?, 0, NOW())");
    return $stmt->execute([$chat_id]);
}

// 📌 افزودن معرفی (زیرمجموعه‌گیری)
function addReferral($chat_id, $referral_id) {
    global $pdo;
    $stmt = $pdo->prepare("UPDATE users SET referrer = ? WHERE chat_id = ?");
    return $stmt->execute([$referral_id, $chat_id]);
}

// 📌 بررسی وضعیت عضویت در کانال و گروه
function checkMembership($chat_id) {
    require "check_membership.php";
    return isUserMember($chat_id);
}

// 📌 دریافت لیست پلن‌های خرید
function getPlans() {
    global $pdo;
    $stmt = $pdo->query("SELECT * FROM plans");
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// 📌 خرید پلن توسط کاربر
function purchasePlan($chat_id, $plan_id) {
    global $pdo;

    // دریافت اطلاعات پلن
    $stmt = $pdo->prepare("SELECT * FROM plans WHERE id = ?");
    $stmt->execute([$plan_id]);
    $plan = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$plan) {
        return "❌ پلن مورد نظر یافت نشد.";
    }

    // بررسی موجودی کیف پول کاربر
    $stmt = $pdo->prepare("SELECT balance FROM users WHERE chat_id = ?");
    $stmt->execute([$chat_id]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user['balance'] < $plan['price']) {
        return "⚠️ موجودی کیف پول شما کافی نیست. لطفاً حساب خود را شارژ کنید.";
    }

    // کاهش موجودی کاربر
    $stmt = $pdo->prepare("UPDATE users SET balance = balance - ? WHERE chat_id = ?");
    $stmt->execute([$plan['price'], $chat_id]);

    // افزودن به لیست خریدهای کاربر
    $stmt = $pdo->prepare("INSERT INTO purchases (chat_id, plan_id, purchased_at, expires_at) VALUES (?, ?, NOW(), DATE_ADD(NOW(), INTERVAL ? DAY))");
    $stmt->execute([$chat_id, $plan_id, $plan['duration']]);

    return "✅ خرید شما با موفقیت انجام شد. مشخصات حساب در بخش **اکانت‌های من** قابل مشاهده است.";
}

// 📌 دریافت حساب‌های خریداری شده کاربر
function getUserAccounts($chat_id) {
    global $pdo;
    $stmt = $pdo->prepare("SELECT p.*, pl.name AS plan_name FROM purchases p INNER JOIN plans pl ON p.plan_id = pl.id WHERE p.chat_id = ?");
    $stmt->execute([$chat_id]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// 📌 بررسی کد تخفیف
function checkCoupon($code) {
    global $pdo;
    $stmt = $pdo->prepare("SELECT discount FROM coupons WHERE code = ?");
    $stmt->execute([$code]);
    $coupon = $stmt->fetch(PDO::FETCH_ASSOC);
    return $coupon ? $coupon['discount'] : false;
}

// 📌 اعمال تخفیف برای خرید
function applyDiscount($chat_id, $discount) {
    global $pdo;
    $stmt = $pdo->prepare("UPDATE users SET balance = balance + (balance * ? / 100) WHERE chat_id = ?");
    return $stmt->execute([$discount, $chat_id]);
}

// 📌 مسدود کردن کاربر
function banUser($chat_id) {
    global $pdo;
    $stmt = $pdo->prepare("UPDATE users SET banned = 1 WHERE chat_id = ?");
    return $stmt->execute([$chat_id]);
}

// 📌 بررسی وضعیت سرور
function checkServerStatus($server_address) {
    $ping = shell_exec("ping -c 1 $server_address");
    return (strpos($ping, "1 received") !== false);
}

// 📌 دریافت درآمد کل
function getTotalIncome() {
    global $pdo;
    $stmt = $pdo->query("SELECT SUM(amount) AS total FROM transactions");
    $result = $stmt->fetch(PDO::FETCH_ASSOC);
    return $result['total'] ?? 0;
}

// 📌 دریافت لیست تراکنش‌های اخیر
function getRecentTransactions() {
    global $pdo;
    $stmt = $pdo->query("SELECT * FROM transactions ORDER BY created_at DESC LIMIT 5");
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// 📌 دریافت کاربران با اکانت در حال انقضا
function getExpiringUsers() {
    global $pdo;
    $stmt = $pdo->query("SELECT chat_id FROM purchases WHERE expires_at <= NOW() + INTERVAL 3 DAY");
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// 📌 ارسال پیام همگانی
function sendBroadcastMessage($message) {
    global $pdo;
    $stmt = $pdo->query("SELECT chat_id FROM users");
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        sendMessage($row['chat_id'], $message);
    }
}
?>
