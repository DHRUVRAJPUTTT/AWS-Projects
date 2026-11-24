
#!/bin/bash
set -e

echo "Validating application deployment"

systemctl is-active --quiet nginx
curl -f http://localhost/

echo "Application validation successful"
