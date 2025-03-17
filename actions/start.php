<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";
require "../libs/check_membership.php"; // 🔹 بررسی عضویت

if (!userExists($chat_id)) {
    addUser($chat_id);
    sendMessage($chat_id, "✅ خوش آمدید! حساب شما با موفقیت ایجاد شد.");
    
    if (isset($referral_id)) {
        addReferral($chat_id, $referral_id);
        sendMessage($referral_id, "🎉 شخص جدیدی از طریق لینک شما ثبت‌نام کرد! به کیف پول شما پاداش اضافه شد.");
    }
} else {
    sendMessage($chat_id, "📌 شما قبلاً ثبت‌نام کرده‌اید!");
}

if (!isUserMember($chat_id)) {
    sendMessage($chat_id, "⚠️ برای استفاده از ربات، لطفاً ابتدا در کانال و گروه زیر عضو شوید:\n\n📢 کانال: [عضویت در کانال](" . $config['required_channel'] . ")\n👥 گروه: [عضویت در گروه](" . $config['required_group'] . ")", true);
    exit;
}

// اگر عضو بود، ادامه اجرای ربات
sendMessage($chat_id, "✅ خوش آمدید! شما به ربات دسترسی دارید.");
?>
