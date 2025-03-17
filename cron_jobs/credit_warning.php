<?php
require "../config.php";
require "../libs/db.php";
require "../libs/ibsng_api.php";
require "../libs/bot_functions.php";

$users = getAllUsers();

foreach ($users as $user) {
    $info = getAccountInfo($user['chat_id']);
    
    if ($info['credit'] < 1) { 
        sendMessage($user['chat_id'], "⚠️ هشدار! حجم اینترنت شما کم است. لطفاً تمدید کنید.");
    }
}
?>
