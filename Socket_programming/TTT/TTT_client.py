import socket
import random

class TTT_Clinet_Communication(object):
    """Create Network interface between server and client"""
    def __init__(self,port,addr = "localhost"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.addr = addr

    def bind(self):
        try:
            self.sock.bind((self.addr,self.port))

        except Exception:
            print("Error in socket bind", Exception)
            return

    def sock_close(self):
        self.sock.close()

    def connect_to_server(self,port,addr = "localhost"):
        try:
            self.sock.connect((addr,port))
        except Exception as e:
            print(e)

    def send(self,msg):
        self.sock.send(msg.encode())

    def recv(self):
        msg = self.sock.recv(4096).decode()
        return msg

    def close(self):
        self.sock.shutdown()
        self.sock.close()

class client_game(TTT_Clinet_Communication):

    def __init__(self,port):
        TTT_Clinet_Communication.__init__(self,port)

    def game_setup(self):
        self.bind()
        self.connect_to_server(12000)

    def start(self):
        self.game_setup()
        rec_msg = self.recv()
        print(rec_msg)
        stop_msg_type = ["Winner","Loser","DRAW"]
        while rec_msg not in stop_msg_type:

            if rec_msg[0] == "E":
                self.send(input())

            rec_msg = self.recv()
            print(rec_msg)

        return rec_msg


def main():
    port = random.randrange(15000,16000)
    client = client_game(port)
    rec_msg = client.start()
    print(rec_msg)
    print("GAME ENDS!! Thanks for playing")


if __name__ == '__main__':
    main()










