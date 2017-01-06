import socket

server = "pythonprogramming.net"
def port_scan(port):
    global server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server, port))
        return True
    except:
        return False

def main():
    for x in range(1,30):
        if port_scan(x):
            print("Port",x,"is open !!!!")
        else:
            print("Port", x, "is closed")

if __name__ == '__main__':
    main()