#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages
install_packages() {
    echo "Installing required packages..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv mysql-server mysql-client certbot phpmyadmin nginx
}

# Function to setup MySQL
setup_mysql() {
    echo "Setting up MySQL..."
    sudo mysql -e "CREATE DATABASE $db_name;"
    sudo mysql -e "CREATE USER '$db_user'@'localhost' IDENTIFIED BY '$db_pass';"
    sudo mysql -e "GRANT ALL PRIVILEGES ON $db_name.* TO '$db_user'@'localhost';"
    sudo mysql -e "FLUSH PRIVILEGES;"
}

# Function to setup SSL
setup_ssl() {
    echo "Setting up SSL..."
    sudo certbot --nginx -d $domain --non-interactive --agree-tos --email $admin_email
    echo "0 0 1 */2 * certbot renew --quiet" | sudo tee -a /etc/cron.d/certbot-renew
}

# Function to setup Python environment
setup_python_env() {
    echo "Setting up Python environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
}

# Function to setup Nginx
setup_nginx() {
    echo "Setting up Nginx..."
    sudo cp nginx.conf /etc/nginx/sites-available/$domain
    sudo ln -s /etc/nginx/sites-available/$domain /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
}

# Function to setup PHPMyAdmin
setup_phpmyadmin() {
    echo "Setting up PHPMyAdmin..."
    sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin
    sudo systemctl restart nginx
}

# Function to setup the bot
setup_bot() {
    echo "Setting up the bot..."
    python3 create_tables.py
    python3 bot.py &
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