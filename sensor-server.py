import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.settimeout(10)
serversocket.bind(('0.0.0.0', 5678))
serversocket.listen(1)

connection, address = serversocket.accept()
while True:
    buf = connection.recv(100) # size of each sensor data packet
    if len(buf) > 0:
        data = (buf.decode().replace(" ",""))
        d = data.split(":")
        t = d[0]
        x = d[1].split(",")[0]
        y = d[1].split(",")[1]
        z = d[1].split(",")[2]
        print("timestamp:",t.ljust(20),"|X:",x.ljust(20),"|Y:",y.ljust(20),"|Z:",z.ljust(20),end="\r")
            
