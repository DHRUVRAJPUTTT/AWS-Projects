
#!/bin/bash
set -e

echo "Starting BeforeInstall hook"

apt-get update -y
apt-get install -y nginx curl

mkdir -p /var/www/html

echo "BeforeInstall completed successfully"
