<?php
require "../config.php";
require "../libs/db.php";
require "../libs/bot_functions.php";
require "../libs/ibsng_api.php";

$servers = getAllServers();
$message = "💻 **وضعیت سرورها:**\n";

foreach ($servers as $server) {
    $status = checkServerStatus($server['address']);
    $message .= "🖥 **{$server['name']}** - " . ($status ? "✅ فعال" : "❌ غیر فعال") . "\n";
}

sendMessage($config['admin_id'], $message);
?>
