#!/bin/bash

# Function to send a message to Discord
escape_message() {
    echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/$/\\n/g'
}

# Function to send message to Discord with escaped content
send_to_discord() {
    local message=$(escape_message "$1")
    echo $message
    current_folder=$(pwd)
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{\"content\":\"$current_folder : $message\"}" \
         "https://discord.com/api/webhooks/1328763919363477524/CnA6ZInh1EtZlu8oXp3kfFhjAb_uqViic8TfLNbmrjwHXPkOmkm9ZkM6JRGh7-Hc4Y2H"
}

#VENV_DIR="venv"

# Check if the virtual environment directory exists
#if [ ! -d "$VENV_DIR" ]; then
    #send_to_discord "Virtual environment not found. Creating one..."
    #python -m venv "$VENV_DIR"
#else
    #send_to_discord "Virtual environment directory already exists."
#fi

# Activate the virtual environment
#send_to_discord "Activating virtual environment."
#source "$VENV_DIR/bin/activate"
#is_venv=$(python -c 'import sys; print(sys.prefix != sys.base_prefix)')
#send_to_discord "Is in virtual environment: $is_venv"

send_to_discord "Updating apt list"
echo -e "deb http://archive.debian.org/debian stretch main contrib non-free\ndeb http://archive.debian.org/debian-security stretch/updates main contrib non-free" | tee /etc/apt/sources.list > /dev/null
apt-get update
send_to_discord "Updated apt list"

send_to_discord "Running apt-get install -y libglib2.0-0"
apt-get install -y libglib2.0-0
send_to_discord "Installed"

send_to_discord "Running apt-get install -y libgl1-mesa-glx"
apt-get install -y libgl1-mesa-glx
send_to_discord "Installed"

send_to_discord "Installing Git"
apt-get install -y git
send_to_discord "InstalledGit"

send_to_discord "Cloning repo https://github.com/Shanksu7/flaskapi.git into folder app..."
git clone https://github.com/Shanksu7/flaskapi.git app
send_to_discord "Cloned repository."
send_to_discord "Moving to /app"
cd app
git pull
send_to_discord "Pulled repo"

# Install main requirements (capture output)
send_to_discord "Installing main requirements..."
pip install -r /home/site/wwwroot/app/requirements.txt
send_to_discord "Installed main requirements."

send_to_discord "Moving files to /home/site/wwwroot/..."
cp -rf /home/site/wwwroot/app/* /home/site/wwwroot/

send_to_discord "Moving to /home/site/wwwroot/"
cd /home/site/wwwroot/

send_to_discord "removing /home/site/wwwroot/app"
rm -r app
send_to_discord "Giving execution rights to startup.sh"
chmod -x startup.sh
# Start the FastAPI app with Gunicorn (capture output)
#echo "Starting FastAPI app guvicorn..."
#
#python -m uvicorn main:app --host 0.0.0.0

ss_output=$(ss -tulnp | grep :8000)

# Check if output exists (i.e., if port 8000 is being used)
if [[ -z "$ss_output" ]]; then
    send_to_discord "Port 8000 is not in use."
    send_to_discord "Running application uvicorn app:app..."
    GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' -c /opt/startup/gunicorn.conf.py --chdir=/home/site/wwwroot" uvicorn app:app
else
    send_to_discord "The following processes are using port 8000:\n$ss_output"
fi

send_to_discord "Finished"
