<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$chat_id = $_POST['chat_id'];
$amount = $_POST['amount'];

if (addWalletBalance($chat_id, $amount)) {
    sendMessage($chat_id, "✅ مبلغ **$amount تومان** به کیف پول شما اضافه شد.");
    sendMessage($config['admin_id'], "✅ واریز تأیید شد و مبلغ **$amount** اضافه گردید.");
} else {
    sendMessage($config['admin_id'], "⛔ خطا در افزودن موجودی.");
}
?>
