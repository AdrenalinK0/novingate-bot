#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to display error messages
error() {
    echo -e "\033[1;31mError: $1\033[0m"
    exit 1
}

# Function to install packages
install_packages() {
    echo "Installing required packages..."
    sudo apt-get update || error "Failed to update package list."
    sudo apt-get install -y python3 python3-pip python3-venv mysql-server mysql-client certbot phpmyadmin nginx || error "Failed to install required packages."
}

# Function to setup MySQL
setup_mysql() {
    echo "Setting up MySQL..."
    sudo mysql -e "CREATE DATABASE IF NOT EXISTS $db_name;" || error "Failed to create database."
    sudo mysql -e "CREATE USER IF NOT EXISTS '$db_user'@'localhost' IDENTIFIED BY '$db_pass';" || error "Failed to create user."
    sudo mysql -e "GRANT ALL PRIVILEGES ON $db_name.* TO '$db_user'@'localhost';" || error "Failed to grant privileges."
    sudo mysql -e "FLUSH PRIVILEGES;" || error "Failed to flush privileges."
}

# Function to setup SSL
setup_ssl() {
    echo "Setting up SSL..."
    sudo certbot --nginx -d $domain --non-interactive --agree-tos --email $admin_email || error "Failed to setup SSL."
    echo "0 0 1 */2 * certbot renew --quiet" | sudo tee -a /etc/cron.d/certbot-renew || error "Failed to setup SSL renewal."
}

# Function to setup Python environment
setup_python_env() {
    echo "Setting up Python environment..."
    python3 -m venv venv || error "Failed to create virtual environment."
    source venv/bin/activate || error "Failed to activate virtual environment."
    pip install -r requirements.txt || error "Failed to install Python packages."
}

# Function to setup Nginx
setup_nginx() {
    echo "Setting up Nginx..."
    sudo cp nginx.conf /etc/nginx/sites-available/$domain || error "Failed to copy Nginx configuration."
    sudo ln -sf /etc/nginx/sites-available/$domain /etc/nginx/sites-enabled/ || error "Failed to create Nginx symlink."
    sudo nginx -t || error "Nginx configuration test failed."
    sudo systemctl restart nginx || error "Failed to restart Nginx."
}

# Function to setup PHPMyAdmin
setup_phpmyadmin() {
    echo "Setting up PHPMyAdmin..."
    sudo ln -sf /usr/share/phpmyadmin /var/www/html/phpmyadmin || error "Failed to create PHPMyAdmin symlink."
    sudo systemctl restart nginx || error "Failed to restart Nginx."
}

# Function to setup the bot
setup_bot() {
    echo "Setting up the bot..."
    python3 create_tables.py || error "Failed to create database tables."
    
    # اجرای ربات در پس‌زمینه و ذخیره خروجی در فایل log
    nohup python3 bot.py > bot.log 2>&1 &
    if [ $? -ne 0 ]; then
        error "Failed to start the bot."
    fi
}

# Main script
echo "Welcome to Novingate Bot Installation Script"

# Get user inputs
read -p "Enter your domain name: " domain
read -p "Enter your bot token: " bot_token
read -p "Enter your admin ID: " admin_id
read -p "Enter your database name: " db_name
read -p "Enter your database username: " db_user
read -p "Enter your database password: " db_pass
read -p "Enter your admin email: " admin_email

# Install required packages
install_packages

# Setup MySQL
setup_mysql

# Setup SSL
setup_ssl

# Setup Python environment
setup_python_env

# Setup Nginx
setup_nginx

# Setup PHPMyAdmin
setup_phpmyadmin

# Setup the bot
setup_bot

echo "Installation completed successfully!"
echo "Your bot is now running on https://$domain"
echo "You can access PHPMyAdmin at https://$domain/phpmyadmin"