
#!/bin/bash
set -e

echo "Starting ApplicationStart hook"

systemctl enable nginx
systemctl restart nginx

echo "Nginx started successfully"
