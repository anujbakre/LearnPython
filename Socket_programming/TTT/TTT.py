import socket
import threading
import time

class TTT_server(object):
    """Create Network interface between server and client"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self,port):
        try:
            self.sock.bind(("localhost",port))
            self.sock.listen(2)
        except Exception:
            print("Error in socket bind", Exception)
            return

    def sick_close(self):
        self.sock.close()



class manage_game(TTT_server):
    """manages server side Game, check for clients and assign players"""

    def __init__(self):
        TTT_server.__init__(self)

    def new_players(self):
        self.waiting_players = []
        self.lock_for_match = threading.Lock()

        while True:

            client_socket = self.sock.accept()

            new_player = player(client_socket)
            self.waiting_players.append(new_player)

            try:
                threading.Thread(target=self.client_thread, args=(new_player)).start()
            except Exception:
                print("Error in thread")


    def client_thread(self,player):
        try:
            player.send("$ Connection Success !!!")

            while player.is_waiting:
                opposition = self.find_opposition(player)

                if opposition is None:
                    time.sleep(1)
                else:
                    new_game = Game(player,opposition)
                    new_game.start()
                    player.status(player.status)
                    opposition.status(opposition.status)
                    player.socket.close()
                    opposition.socket.close()

        except Exception:
            print("Error in client thread")

    def find_opposition(self,player):
        self.lock_for_match()
        for opposition in self.waiting_players:
            if opposition.is_waiting and opposition != player:
                opposition.is_waiting = False
                player.is_waiting = False
                return opposition



class player:

    count = 0
    def __init__(self,client_sock):
        player.count += 1
        self.id = player.count
        self.socket = client_sock
        self.is_waiting = True
        self.game_id = None
        self.my_turn = False
        self.mark = ""
        self.status = ""

    def send(self,msg):
        self.socket.send(msg.encode())

    def recv(self):
        rec_msg = self.socket.recv(4096).decode
        return int(rec_msg)

class Game:
    game = 100

    def __init__(self,player1, player2):
        Game.game += 1
        self.game_id = Game.game
        player1.game_id = player2.game_id= self.game_id
        player1.mark = "X"
        player2.mark = "O"
        self.player_1 = player1
        self.player_2 = player2
        self.game_board = ['-']*9

    def start(self):
        self.player_1.send("You are playing against player id",self.player_2.id)
        self.player_2.send("You are playing against player id", self.player_1.id)


        while True:
            if self.move(self.player_1,self.player_2):
                return
            if self.move(self.player_2,self.player_1):
                return


    def enter_on_board(self,pos, playing, waiting):
        self.game_board[pos] = playing.mark
        playing.send(self.display_board())
        waiting.send(self.display_board())
        return self.check_winner(playing, waiting)



    def move(self,playing, waiting):
        playing.my_turn = True
        waiting.my_turn = False

        playing.send("Enter The position to put your sign")
        pos = playing.recv()
        return self.enter_on_board(pos, playing)


    def check_winner(self,player, waiting):
        s = self.game_board
        # Check columns
        if s[0] == s[1] ==s[2] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True
        if s[3]==s[4]==s[5] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True
        if s[6] == s[7] == s[8] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True

        # Check rows

        if s[0] == s[3] == s[6] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True
        if s[1] == s[4] == s[7] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True
        if s[2] == s[5] == s[8] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True

        # Check diagonal
        if s[0] == s[4] == s[8] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True
        if s[2] == s[4] == s[6] == player.mark:
            player.status = "Winner"
            waiting.status = "Loser"
            return True

        #check if board is full
        if "-" not in s:
            player.status = "DRAW"
            waiting.status = "DRAW"
            return True

        return False

    def display_board(self):
        pass


def main():
    game_server = manage_game()
    game_server.bind(12000)

    # now wait for clients to connect and play game
    game_server.new_players()





if __name__ == '__main__':
    main()

