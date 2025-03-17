<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$code = $_POST['code'];
$discount = $_POST['discount'];

if (addCoupon($code, $discount)) {
    sendMessage($config['admin_id'], "✅ کد تخفیف **$code** با مقدار **$discount%** اضافه شد.");
} else {
    sendMessage($config['admin_id'], "⛔ خطا در افزودن کد تخفیف!");
}
?>
