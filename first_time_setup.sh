python3 -m venv /home/site/wwwroot/antenv
source "/home/site/wwwroot/antenv/bin/activate"
echo -e "deb http://archive.debian.org/debian stretch main contrib non-free\ndeb http://archive.debian.org/debian-security stretch/updates main contrib non-free" | tee /etc/apt/sources.list > /dev/null
apt-get update
apt-get install -y git
git clone https://github.com/Shanksu7/flaskapi app
cd app
git pull
cp -rf /home/site/wwwroot/app/* /home/site/wwwroot/
cd /home/site/wwwroot/
rm -r app
chmod -x startup.sh
pip install -r requirements.txt
deactivate
