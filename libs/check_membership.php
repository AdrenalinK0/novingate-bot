<?php
require "../config.php";
require "bot_functions.php";

function isUserMember($chat_id) {
    global $config;
    
    $channel = $config["required_channel"];
    $group = $config["required_group"];
    $bot_token = $config["bot_token"];

    // چک عضویت در کانال
    $channel_status = file_get_contents("https://api.telegram.org/bot$bot_token/getChatMember?chat_id=$channel&user_id=$chat_id");
    $channel_data = json_decode($channel_status, true);

    // چک عضویت در گروه (اگر نیاز باشد)
    $group_status = file_get_contents("https://api.telegram.org/bot$bot_token/getChatMember?chat_id=$group&user_id=$chat_id");
    $group_data = json_decode($group_status, true);

    // بررسی وضعیت عضویت
    $is_channel_member = isset($channel_data["result"]["status"]) && in_array($channel_data["result"]["status"], ["member", "administrator", "creator"]);
    $is_group_member = isset($group_data["result"]["status"]) && in_array($group_data["result"]["status"], ["member", "administrator", "creator"]);

    return $is_channel_member && $is_group_member;
}
?>
