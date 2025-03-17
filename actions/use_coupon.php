<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$code = $_POST['code'];
$discount = checkCoupon($code);

if ($discount) {
    sendMessage($chat_id, "🎉 کد تخفیف شما اعمال شد! **$discount%** تخفیف دریافت کردید.");
    applyDiscount($chat_id, $discount);
} else {
    sendMessage($chat_id, "⛔ کد تخفیف نامعتبر است!");
}
?>
