<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";

$income = getTotalIncome();
$transactions = getRecentTransactions();

$message = "📊 **گزارش مالی:**\n";
$message .= "💰 درآمد کل: **$income تومان**\n\n";
$message .= "🔄 **تراکنش‌های اخیر:**\n";
foreach ($transactions as $txn) {
    $message .= "🟢 **مبلغ:** {$txn['amount']} تومان\n📅 **تاریخ:** {$txn['date']}\n———————————\n";
}

sendMessage($config['admin_id'], $message);
?>
