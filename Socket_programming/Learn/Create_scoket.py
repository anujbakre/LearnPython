import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)


server = 'usc.edu'
port = 80
request = "GET / HTTP/1.1\nHost: "+server+"\n\n"

s.connect((server,port))
s.send(request.encode())
result = s.recv(10).decode()


while len(result) > 0:
    print(result)
    result = s.recv(10).decode()