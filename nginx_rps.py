#!/anaconda3/bin/python3
import sys
import re
import requests
import socket
from time import sleep
import datetime
    
prev_hand_req = 0
hostname = socket.gethostname()
url = sys.argv[1]
threshold = int(sys.argv[2])
interval = int(sys.argv[3])

while True:
    x = datetime.datetime.now()
    r = requests.get(url)
    output = r.text
    match = re.search(r'(\d+)\s(\d+)\s(\d+)', output)
    curr_hand_req = int(match.group(3))
    
    if prev_hand_req == 0:
        prev_hand_req = curr_hand_req
    else:
        nginx_rps = (curr_hand_req - prev_hand_req)
        print(f"request per second = {nginx_rps}")       
        prev_hand_req = curr_hand_req
        if (nginx_rps >= threshold):
            with open ("alerts_%s.log" %hostname, mode="a") as f:
                f.write(x.strftime('%d %b %Y %H:%M:%S'))
                f.write("\t")
                f.write("Alert!! \t")
                f.write(str(nginx_rps))
                f.write("\n")
    sleep(interval)
