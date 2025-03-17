<?php
require "../config.php"; // دریافت اطلاعات دیتابیس از فایل تنظیمات

try {
    // اتصال به دیتابیس با PDO
    $pdo = new PDO("mysql:host=" . $config['db_host'] . ";dbname=" . $config['db_name'] . ";charset=utf8", $config['db_user'], $config['db_pass']);
    
    // تنظیمات برای نمایش خطاهای PDO
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    die("❌ خطا در اتصال به دیتابیس: " . $e->getMessage());
}

// 📌 بررسی وجود جدول‌ها و ایجاد آن‌ها در صورت نبودن
function setupDatabase() {
    global $pdo;

    $queries = [
        // جدول کاربران
        "CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id BIGINT UNIQUE NOT NULL,
            balance INT DEFAULT 0,
            referrer BIGINT DEFAULT NULL,
            banned TINYINT DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )",

        // جدول پلن‌های فروش
        "CREATE TABLE IF NOT EXISTS plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price INT NOT NULL,
            duration INT NOT NULL, -- روزهای اعتبار
            max_users INT NOT NULL
        )",

        // جدول خریدهای کاربران
        "CREATE TABLE IF NOT EXISTS purchases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            plan_id INT NOT NULL,
            purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE CASCADE,
            FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
        )",

        // جدول تراکنش‌ها
        "CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            amount INT NOT NULL,
            type ENUM('deposit', 'withdrawal', 'purchase') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE CASCADE
        )",

        // جدول کدهای تخفیف
        "CREATE TABLE IF NOT EXISTS coupons (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(50) UNIQUE NOT NULL,
            discount INT NOT NULL,
            expires_at TIMESTAMP NOT NULL
        )",

        // جدول سرورهای iBANG
        "CREATE TABLE IF NOT EXISTS servers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            address VARCHAR(255) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        )",

        // جدول تیکت‌های پشتیبانی
        "CREATE TABLE IF NOT EXISTS tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            message TEXT NOT NULL,
            status ENUM('open', 'closed') DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES users(chat_id) ON DELETE CASCADE
        )"
    ];

    // اجرای کوئری‌های ایجاد جدول
    foreach ($queries as $query) {
        $pdo->exec($query);
    }
}

// اجرای تابع ایجاد جدول‌ها
setupDatabase();
?>
