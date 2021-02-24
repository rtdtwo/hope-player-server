git pull
pip3 install -r requirements.txt
sudo kill -9 $(sudo lsof -t -i:7474)
export GENIUS_ACCESS_TOKEN="8qDu_WbDrRyUFQwWDEgJG5elp92ZuIA6BRoVzKAM3Wx1Wu5169IOM_E3PqMPlziM"
nohup python3 main.py &