import socket
import random

class SW_Server(object):
    def __init__(self, buffer_size = 1024, port = 15000, tagret = 'localhost'):
        self.buffer_size = buffer_size
        self.port = port
        self.target = tagret

    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.target, self.port))
        return self.s


def pack_drop(value):
    if value == 0:
        return False
    x = random.randrange(100)
    tmp = 100 // value
    if x % tmp == 0:
        return True
    return False

def main():

    server = SW_Server()
    s = server.create_socket()
    packet_drop_percent = 20
    send_msg = "ACK"

    while True:
        rec_msg, addr = s.recvfrom(server.buffer_size)
        if not pack_drop(packet_drop_percent):
            print("Frame",rec_msg.decode()," recived from",addr,"successfully")
            send_msg = "ACK"

        else:
            print("Message",rec_msg.decode(),"dropped due errors")
            send_msg = "NAK"

        s.sendto(send_msg.encode(),addr)

if __name__ == '__main__':
    main()


