#!/bin/bash

# Function to send a message to Discord
escape_message() {
    echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/$/\\n/g'
}

send_to_discord() {
    local message=$(escape_message "$1")
    echo "$message"
    current_folder=$(pwd)
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{\"content\":\"$current_folder : $message\"}" \
         "https://discord.com/api/webhooks/1328763919363477524/CnA6ZInh1EtZlu8oXp3kfFhjAb_uqViic8TfLNbmrjwHXPkOmkm9ZkM6JRGh7-Hc4Y2H"
}

# Persistent virtual environment directory
VENV_DIR="/home/venv"

# Check and create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    send_to_discord "Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_DIR"
else
    send_to_discord "Virtual environment directory already exists."
fi

# Activate the virtual environment
send_to_discord "Activating virtual environment."
source "$VENV_DIR/bin/activate"
is_venv=$(python -c 'import sys; print(sys.prefix != sys.base_prefix)')
send_to_discord "Is in virtual environment: $is_venv $VENV_DIR"

# Ensure required system packages are installed
send_to_discord "Updating and installing required packages..."
REQUIRED_PACKAGES=("git" "libglib2.0-0" "libgl1-mesa-glx")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! dpkg -s "$pkg" &> /dev/null; then
        apt-get update
        apt-get install -y "$pkg"
        send_to_discord "Installed $pkg."
    else
        send_to_discord "$pkg is already installed."
    fi
done

# Clone or update the repository
REPO_URL="https://github.com/Shanksu7/flaskapi.git"
APP_DIR="/home/site/wwwroot/app"
send_to_discord "Checking repository..."
if [ ! -d "$APP_DIR" ]; then
    send_to_discord "Cloning repo $REPO_URL into $APP_DIR..."
    git clone "$REPO_URL" "$APP_DIR"
else
    send_to_discord "Repository already exists. Pulling updates."
    cd "$APP_DIR" && git pull && cd -
fi

# Install Python requirements
REQUIREMENTS_FILE="$APP_DIR/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    send_to_discord "Installing Python requirements..."
    pip install -r "$REQUIREMENTS_FILE"
    send_to_discord "Installed Python requirements."
else
    send_to_discord "Requirements file not found. Skipping Python dependencies installation."
fi

# Move files to /home/site/wwwroot/
TARGET_DIR="/home/site/wwwroot"
send_to_discord "Checking application files..."
if [ ! -f "$TARGET_DIR/startup.sh" ]; then
    send_to_discord "Moving files to $TARGET_DIR..."
    cp -rf "$APP_DIR"/* "$TARGET_DIR/"
else
    send_to_discord "Files are already in $TARGET_DIR. Skipping copy."
fi

# Remove app directory after moving files
if [ -d "$APP_DIR" ]; then
    send_to_discord "Removing $APP_DIR..."
    rm -rf "$APP_DIR"
fi

# Make the startup script executable
STARTUP_SCRIPT="$TARGET_DIR/startup.sh"
if [ -f "$STARTUP_SCRIPT" ]; then
    send_to_discord "Making startup script executable..."
    chmod +x "$STARTUP_SCRIPT"
fi

# Check if port 8000 is in use and start the application if not
send_to_discord "Checking if port 8000 is in use..."
ss_output=$(ss -tulnp | grep :8000)

if [[ -z "$ss_output" ]]; then
    send_to_discord "Port 8000 is not in use. Starting application."
    GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' -c /opt/startup/gunicorn.conf.py --chdir=/home/site/wwwroot"
    gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app
else
    send_to_discord "Port 8000 is already in use. Skipping application start. Details:\n$ss_output"
fi

send_to_discord "Script finished."
