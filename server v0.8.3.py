import socket
import rsa
import random
import json
from time import sleep
from threading import Thread
from datetime import datetime
from copy import deepcopy
from check_module import *
class EventLoop(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.events2 = []
        self.delay = 0.1
        self.tickrate = int(1/self.delay)
        self.active_games = []
        self.ready_pairs = []
        
        
    def find_pair(self):
        try:
            first_player = waiting_clients[0]
            second_player = waiting_clients[1]
            self.ready_pairs.append((first_player, second_player))
            waiting_clients.remove(first_player)
            waiting_clients.remove(second_player)
            first_player.send_msg('READY')
            second_player.send_msg('READY')
        except IndexError:
            pass

    def check_ready_pairs(self):
        to_delete = []
        for first,second in self.ready_pairs:
            if first.accepted and second.accepted:
                if random.randint(0,1):
                    new_game = Game(first,second)
                else:
                    new_game = Game(second, first)
                self.active_games.append(new_game)
                first.game = new_game
                second.game = new_game
                new_game.white_player.send_msg('GAME')
                new_game.white_player.send_msg('MSG You plays first')
                new_game.black_player.send_msg('GAME')
                new_game.black_player.send_msg('MSG Opponent plays first')
                to_delete.append((first, second))
        for pair in to_delete:
            self.ready_pairs.remove(pair)

    def run(self) -> None:
        while True:
            sleep(self.delay)
            self.find_pair()
            self.check_ready_pairs()
            for event2 in self.get_events2():
                if event2['type'] == 'select':
                    if event2['caller'].game:
                        event2['caller'].game.do_step(event2['caller'], event2['x'], event2['y'])
                elif event2['type'] == 'accept':
                    if event2['caller'].game == None:
                        event2['caller'].accepted = True
                    else:
                        event2['caller'].send_msg('MSG game already accepted')


    def get_events2(self):
        events2 = self.events2[:]
        self.events2 = []
        return events2
        
    def add_event2(self,event):
        self.events2.append(event)
            

def get_date() -> str:
    date = datetime.now()
    date_str = '[{0:0>2}-{1:0>2}-{2:0>4} {3:0>2}:{4:0>2}]'.format(date.day,
                                                                  date.month,
                                                                  date.year,
                                                                  date.hour,
                                                                  date.minute)
    return date_str


class ConnectedClient(Thread):

    def __init__(self, socket, address):
        Thread.__init__(self)
        self.address = address
        self.socket = socket
        self.xor_key = None
        self.name = 'User' + str(users)
        self.accepted = False
        self.connected = False
        self.exceed_time = 10
        self.game = None

        
    def disconnect(self, msg):
        print(get_date(), msg, self.address)
        self.connected  = False
        if self.game:
            if self.game.white_player == self:
                self.game.black_player.send_msg('END Your opponent disconnected. You automatically win')
                self.game.black_player.game = None
            else:
                self.game.white_player.send_msg('END Your opponent disconnected. You automatically win')
                self.game.white_player.game = None
            loop.active_games.remove(self.game)
        elif self in waiting_clients:
            waiting_clients.remove(self)
        for pair in loop.ready_pairs:
            if self in pair:
                if self == pair[0]:
                    pair[1].send_msg('CANCEL Your opponent disconnected')
                else:
                    pair[0].send_msg('CANCEL Your opponent disconnected')
                break
            loop.ready_pairs.remove(pair)
        connected_clients.remove(self)


    def xor_crypt(self, string:bytes, key:bytes) -> bytes:
        key_len = len(key)
        fitted_key = bytes(key[index % key_len] for index in range(len(string)))
        crypto_str = bytes([string[index] ^ fitted_key[index] for index in range(len(string))])
        return crypto_str


    def get_msg(self):
        chunks = []
        bytes_recv = 0
        while bytes_recv < 512:
            try:
                chunk = self.socket.recv(min(512 - bytes_recv, 2048))
            except ConnectionError:
                return False
            if chunk == b'':
                return False
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return self.xor_crypt(b''.join(chunks), self.xor_key).decode('utf-8').strip()


    def send_msg(self, msg):
        msg = msg + ' ' * (512 - len(msg))
        msg = self.xor_crypt(msg.encode('utf-8'), self.xor_key)
        bytes_sent = 0
        while bytes_sent < 512:
            try:
                sent = self.socket.send(msg[bytes_sent:])
            except ConnectionError:
                return False
            if sent == 0:
                return False
            bytes_sent += sent 
        return True

    def run(self):
        self.socket.send(public.save_pkcs1())
        raw_xor_key = self.socket.recv(1024)
        self.xor_key = rsa.decrypt(raw_xor_key, private)
        print(get_date(),'secure key received from', self.address)
        waiting_clients.append(self)
        self.connected = True
        while self.connected:
            client_data = self.get_msg()
            if not client_data:
                self.disconnect('Connection error')
                break
            data_words = client_data.split(' ')
            print(get_date(), 'get', client_data, 'from', self.address)
            if data_words[0] == 'SELECT':
                loop.add_event2({'type':'select',
                                 'x':int(data_words[1]),
                                 'y':int(data_words[2]),
                                 'caller':self
                                 }
                                )
            elif data_words[0] == 'ACCEPT':
                loop.add_event2({'type':'accept', 'caller':self})
            else:
                self.disconnect('Wrong data')
                print(get_date(), 'can\'t recognize:',client_data, 'from', self.address)
##                loop.add_event({'type':'disconnect','msg':'Wrong data' ,'caller':self})
                break

class Game():

    def __init__(self, first_player, second_player):
        self.white_player  = first_player
        self.black_player = second_player
        self.white_step = True
        self.black_step = False
        self.white_check = False
        self.black_check = False
        self.white_checkmate = False
        self.black_checkmate = False
        self.white_selected_figure = [100,100]
        self.black_selected_figure = [100,100]
        self.field = [
                        ['r','h','b','q','k','b','h','r'],
                        ['p','p','p','p','p','p','p','p'],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' '],
                        ['p','p','p','p','p','p','p','p'],
                        ['r','h','b','q','k','b','h','r'],
                    ]
        self.white_figures = [[j,i] for j in range(8) for i in range(6,8)]
        self.black_figures = [[j,i] for j in range(8) for i in range(2)]
        self.taken_by_white = {'p':0, 'r':0, 'b':0, 'h':0, 'q':0}
        self.taken_by_black = {'p':0, 'r':0, 'b':0, 'h':0, 'q':0}
        self.black_admissible = []
        self.white_admissible = []

    def do_step(self, player, x, y):
        if (0 <= x <= 7) and (0 <= y <= 7):
            if player == self.white_player:
                if self.white_step:
                    if [x, y] in self.white_figures:
                        self.white_selected_figure = [x, y]
                        self.white_admissible = check_positions_white(self.white_selected_figure,
                                                                 self.white_figures,
                                                                 self.black_figures,
                                                                 self.field)
                        figure_type = self.field[y][x]
                        figure_pos = [x,y]
                        self.white_admissible = exclude_check_unprotected(figure_type,
                                                                          figure_pos,
                                                                          self.white_admissible,
                                                                          self.white_figures,
                                                                          self.black_figures,
                                                                          check_positions_black,
                                                                          self.field)                                            
                    elif [x, y] in self.black_figures and self.white_selected_figure:
                        if [x,y] in self.white_admissible:
                            self.take_figure(self.white_figures, self.black_figures, [x,y], self.white_selected_figure)
                            self.white_player.send_msg('TAKE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_player.send_msg('TAKE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.white_admissible = []
                        self.white_selected_figure = [100,100]
                    elif self.field[y][x] == ' ' and self.white_selected_figure:
                        if [x,y] in self.white_admissible:
                            self.move_figure(self.white_figures, [x,y], self.white_selected_figure)
                            self.white_player.send_msg('MOVE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_player.send_msg('MOVE ' + json.dumps([[x,y], self.white_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.white_admissible = []
                        self.white_selected_figure = [100,100]
                    else:
                        self.white_admissible = []
                        self.white_selected_figure = [100,100]
                    self.white_player.send_msg('ADMISSIBLE ' + json.dumps(self.white_admissible))
                    self.white_player.send_msg('LIGHT ' + json.dumps(self.white_selected_figure))
                    self.white_check = check_shah(self.white_figures,
                                                      self.black_figures,
                                                      check_positions_black,
                                                      self.field)
                    self.black_check = check_shah(self.black_figures,
                                                      self.white_figures,
                                                      check_positions_white,
                                                      self.field)
                    self.white_checkmate = check_checkmate(self.white_figures,
                                                               check_positions_white,
                                                               self.black_figures,
                                                               check_positions_black,
                                                               self.field)
                    self.black_checkmate = check_checkmate(self.black_figures,
                                                               check_positions_black,
                                                               self.white_figures,
                                                               check_positions_white,
                                                               self.field)
                    if self.black_checkmate:
                        self.black_player.send_msg('END You lose!')
                        self.white_player.send_msg('END You win!')
                    elif self.white_checkmate:
                        self.white_player.send_msg('END You lose!')
                        self.black_player.send_msg('END You win')
                else:
                    self.white_player.send_msg('ALERT not your step')
            else:
                if self.black_step:
                    if [x, y] in self.black_figures:
                        self.black_selected_figure = [x,y]
                        self.black_admissible = check_positions_black(self.black_selected_figure,
                                                                      self.black_figures,
                                                                      self.white_figures,
                                                                      self.field)
                        figure_type = self.field[y][x]
                        figure_pos = [x, y]
                        self.black_admissible = exclude_check_unprotected(figure_type,
                                                                          figure_pos,
                                                                          self.black_admissible,
                                                                          self.black_figures,
                                                                          self.white_figures,
                                                                          check_positions_white,
                                                                          self.field)
                    elif [x, y] in self.white_figures and self.black_selected_figure:
                        if [x, y] in self.black_admissible:
                            self.take_figure(self.black_figures, self.white_figures, [x,y], self.black_selected_figure)
                            self.white_player.send_msg('TAKE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_player.send_msg('TAKE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.black_admissible = []
                        self.black_selected_figure = [100,100]
                    elif self.field[y][x] == ' ' and self.black_selected_figure:
                        if [x, y] in self.black_admissible:
                            self.move_figure(self.black_figures, [x,y], self.black_selected_figure)
                            self.white_player.send_msg('MOVE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_player.send_msg('MOVE ' + json.dumps([[x,y], self.black_selected_figure]))
                            self.black_step = not self.black_step
                            self.white_step = not self.white_step
                        self.black_admissible = []
                        self.black_selected_figure = [100,100]
                    self.black_player.send_msg('ADMISSIBLE ' + json.dumps(self.black_admissible))
                    self.black_player.send_msg('LIGHT ' + json.dumps(self.black_selected_figure))
                    self.white_check = check_shah(self.white_figures,
                                                      self.black_figures,
                                                      check_positions_black,
                                                      self.field)
                    self.black_check = check_shah(self.black_figures,
                                                      self.white_figures,
                                                      check_positions_white,
                                                      self.field)
                    self.white_checkmate = check_checkmate(self.white_figures,
                                                               check_positions_white,
                                                               self.black_figures,
                                                               check_positions_black,
                                                               self.field)
                    self.black_checkmate = check_checkmate(self.black_figures,
                                                               check_positions_black,
                                                               self.white_figures,
                                                               check_positions_white,
                                                               self.field)
                    if self.black_checkmate:
                        self.black_player.send_msg('END You lose!')
                        self.white_player.send_msg('END You win!')
                    elif self.white_checkmate:
                        self.white_player.send_msg('END You lose!')
                        self.black_player.send_msg('END You win!')
                else:
                    self.black_player.send_msg('ALERT not your step')

   
    def take_figure(self,player_figures, opponent_figures, new_pos, old_pos):
        opponent_figures.remove(new_pos)
        self.field[new_pos[1]][new_pos[0]] = self.field[old_pos[1]][old_pos[0]]
        self.field[old_pos[1]][old_pos[0]] = ' '
        player_figures[player_figures.index(old_pos)] = new_pos[:]


    def move_figure(self,player_figures, new_pos, old_pos):
        self.field[new_pos[1]][new_pos[0]] = self.field[old_pos[1]][old_pos[0]]
        self.field[old_pos[1]][old_pos[0]] = ' '
        player_figures[player_figures.index(old_pos)] = new_pos[:]

     
VERSION = '0.8'
ADDRESS, PORT = '127.0.0.1', 6666
print(get_date(), 'chess game server ' + VERSION + ' running on ' + ADDRESS + ' ' + str(PORT))
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
server_sock.bind((ADDRESS, PORT))
public, private = rsa.newkeys(1024)
print(get_date(), 'key pair generated')
connected_clients = []
waiting_clients = []
playing_clients = []
active_games = []
users = 0
loop = EventLoop()
loop.start()
while True:
    server_sock.listen(0)
    sock,addr = server_sock.accept()
    new_client = ConnectedClient(sock,addr)
    connected_clients.append(new_client)
    new_client.start()
    users += 1
