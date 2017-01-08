# author Anuj Bakre


import socket

class SW_client(object):
    def __init__(self, buffer_size = 8, port = 16000, tagret = 'localhost'):
        self.buffer_size = buffer_size
        self.port = port
        self.target = tagret

    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self.s



def main():
    server_addr = ('localhost',15000)
    clinet = SW_client()
    s = clinet.create_socket()
    lenght = 10
    drop_count = 0
    i = 1
    while i <= lenght:
        s.sendto(str(i).encode(),server_addr)
        rec_msg, addr = s.recvfrom(100)
        rec_msg = rec_msg.decode()
        if rec_msg == "ACK":
            print("Frame",i,"sent correctly !")
            i += 1
        else:
            print("Frame",i,"dropped by server, sending again")
            drop_count += 1


    s.close()

    print("Drop percentage is",(drop_count / lenght)*100,"%")

if __name__ == '__main__':
    main()


