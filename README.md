![VScode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![
](https://img.shields.io/badge/-Linux-grey?logo=linux)
# MQTT-sensor test use
## Base file : 
```bash
File: sender.py and receiver.py, 
MQTT: broker = '149.165.159.142' \ port = 1883, 
VM:   Indiana Jetstream
Test: dashbord.html is the file has three small grah and one large grah.
```
## File:
[Sender.py](https://github.com/UASensorLab/MQTT/blob/main/sender.py) is the one large graph, for run all other three graph.

[Sender2.py](https://github.com/UASensorLab/MQTT/blob/main/sender2.py) is the one on top left,first.

[Sender3.py](https://github.com/UASensorLab/MQTT/blob/main/sender3.py) is the one on middle, second. 
## Timeline update 
11/3 (dashboard.html)
  1. added the second client.
  2. Added the second sender.
  3. Distributed the 3 graphs into separate HTML files called newgraph.
  4. Updated the dashboard.html to remove the addition of the fourth graph.
  5. Updated sender.py to send data to the three graphs.
