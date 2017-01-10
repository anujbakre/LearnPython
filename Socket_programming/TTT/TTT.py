import socket
import threading
import time

class TTT_server_communication(object):
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

    def sock_close(self):
        self.sock.close()



class manage_game(TTT_server_communication):
    """manages server side Game, check for clients and assign players"""

    def __init__(self):
        TTT_server_communication.__init__(self)

    def new_players(self):
        self.waiting_players = []
        self.lock_for_match = threading.Lock()

        while True:

            client_socket,addr = self.sock.accept()
            print("accepted from", addr)

            new_player = player(client_socket)
            self.waiting_players.append(new_player)
            print("new player connected",new_player.id)

            #try:
            threading.Thread(target=self.client_thread, args=(new_player,)).start()
            #except Exception as e:
                #print("Error in thread",e)


    def client_thread(self,player):
        try:
            player.send("$ Connection Success !!!\n Your ID is "+str(player.id))

            while player.is_waiting:
                with self.lock_for_match:
                    opposition = self.find_opposition(player)
                if opposition is None:time.sleep(1)
            #with self.lock_for_match:
            if player.game_id == None:
                new_game = Game(player,opposition)
                print("Game",new_game.game_id,"started betwwen players:", player.id, "and", opposition.id)
                #threading.Thread(target=new_game.start())
                new_game.start()
                print("Game over")
                player.send(player.status)
                opposition.send(opposition.status)
            else:
                while player.status == A:
                    sleep(1)


        except Exception as e:
            print("Error in client thread",e)

    def find_opposition(self,player):
        for opposition in self.waiting_players:
            if opposition.is_waiting and opposition != player:
                if opposition is None: return None
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
        self.mark = "A"
        self.status = "A"


    def send(self,msg):
        self.socket.send(msg.encode())

    def recv(self):
        rec_msg = self.socket.recv(4096).decode()
        return int(rec_msg)

class Game:
    game = 100

    def __init__(self,player1, player2):
        Game.game += 1
        self.game_id = Game.game

        player1.mark = "X"
        player2.mark = "O"
        self.player_1 = player1
        self.player_2 = player2
        self.game_board = ['-']*9
        print(113)
        print("player mark",self.player_1.mark)


    def start(self):
        print("line 116")
        self.player_1.send("You are playing against player id "+str(self.player_2.id)+"Your mark is "+str(self.player_1.mark))
        self.player_2.send("You are playing against player id "+str(self.player_1.id)+"Your mark is "+str(self.player_2.mark))
        print()

        while True:
            if self.move(self.player_1,self.player_2):
                return
            if self.move(self.player_2,self.player_1):
                return




    def enter_on_board(self,pos, playing, waiting):
        print("line 133",playing.mark)
        self.game_board[pos] = playing.mark
        playing.send(self.display_board())
        waiting.send(self.display_board())
        return self.check_winner(playing, waiting)



    def move(self,playing, waiting):
        playing.my_turn = True
        waiting.my_turn = False
        print("turn", playing.id)
        print("waiting", waiting.id)
        playing.send("Enter The position to put your sign:\t")
        waiting.send("Player "+str(playing.id)+" is playing. Please wait for your turn")
        pos = playing.recv()
        print("POS=",pos)
        return self.enter_on_board(pos, playing, waiting)


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
        s = self.game_board
        return ("|" + s[0] + "|" + s[1] + "|" + s[2] + "|\n"
                + "|" + s[3] + "|" + s[4] + "|" + s[5] + "|\n"
                + "|" + s[6] + "|" + s[7] + "|" + s[8] + "|\n")


def main():
    game_server = manage_game()
    game_server.bind(12000)

    # now wait for clients to connect and play game
    game_server.new_players()



if __name__ == '__main__':
    main()

