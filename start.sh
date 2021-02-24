git pull
pip3 install -r requirements.txt
sudo kill -9 $(sudo lsof -t -i:7475)
nohup python3 main.py &