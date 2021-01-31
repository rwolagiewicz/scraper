apt-get install unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get update
apt-get check
apt-get -f -y install
dpkg -i google-chrome-stable_current_amd64.deb
chrome_ver=`google-chrome --version | cut -c15-20`
ver=`curl -s https://chromedriver.storage.googleapis.com/ | grep -oPm1 "(?<=<Key>)[^<]+" | grep "^$chrome_ver.*linux64.zip$" | tail -1`
wget https://chromedriver.storage.googleapis.com/$ver
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
