CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `telegram_id` BIGINT NOT NULL UNIQUE,
    `wallet` INT DEFAULT 0,
    `referral_code` VARCHAR(50),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `accounts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `username` VARCHAR(50),
    `password` VARCHAR(50),
    `expires_at` DATETIME,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

CREATE TABLE `wallet` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `amount` INT NOT NULL,
    `status` ENUM('pending', 'confirmed') DEFAULT 'pending',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

CREATE TABLE plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price INT,
    days INT
);

CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    status ENUM('open', 'closed') DEFAULT 'open'
);

CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    value TEXT
);
