#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! command -v nginx >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary folders
web_static_dir="/data/web_static"
releases_dir="$web_static_dir/releases"
shared_dir="$web_static_dir/shared"
test_dir="$releases_dir/test"
index_file="$test_dir/index.html"

mkdir -p "$web_static_dir" "$releases_dir" "$shared_dir" "$test_dir"
touch "$index_file"
echo "Hello, world!" > "$index_file"

# Create or recreate the symbolic link
symbolic_link="/data/web_static/current"
if [ -L "$symbolic_link" ]; then
    rm -f "$symbolic_link"
fi
ln -s "$test_dir" "$symbolic_link"

# Give ownership of the /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Set ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_content=$(cat <<EOM
server {
    listen 80;
    listen [::]:80;

    location /hbnb_static {
        alias $symbolic_link/;
        index index.html;
    }
}
EOM
)
echo "$config_content" > "$config_file"

# Restart Nginx
service nginx restart

