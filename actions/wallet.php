<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$wallet = getWalletBalance($chat_id);

$message = "💰 **موجودی کیف پول شما:** `$wallet` تومان\n\n";
$message .= "📌 برای افزایش موجودی، مبلغی بیشتر از **30,000 تومان** واریز کنید.";
sendMessage($chat_id, $message);
?>
