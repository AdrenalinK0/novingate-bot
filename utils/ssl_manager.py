import subprocess

def setup_ssl(domain):
    subprocess.run(["sudo", "certbot", "--nginx", "-d", domain])

def renew_ssl(domain):
    subprocess.run(["sudo", "certbot", "renew", "--nginx", "-d", domain])