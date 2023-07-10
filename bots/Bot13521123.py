import random
from game import Board
import globals as globals

class Bot13521123(object):
    """
    Bot player
    """

    def __init__(self):
        self.player = None

        """
            TODO: Ganti dengan NIM kalian
        """
        self.NIM = "13521123"

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, return_var):
        try:
            location = self.get_input(board)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1

        counterr = 0
        while move == -1 or move not in board.availables:
            if counterr > 1000000:
                return
            if globals.stop_threads:
                return
            try:
                location = self.get_input(board)
                if isinstance(location, str):  # for python3
                    location = [int(n, 10) for n in location.split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
                counterr += 1

        return_var.append(move) 

    def __str__(self):
        return "{} a.k.a Player {}".format(self.NIM,self.player)

            
    def get_input(self, board : Board) -> str:
        """
            Parameter board merepresentasikan papan permainan. Objek board memiliki beberapa
            atribut penting yang dapat menjadi acuan strategi.
            - board.height : int (x) -> panjang papan
            - board.width : int (y) -> lebar papan
            Koordinat 0,0 terletak pada kiri bawah

            [x,0] [x,1] [x,2] . . . [x,y]                               
            . . . . . . . . . . . . . . .  namun perlu diketahui        Contoh 4x4: 
            . . . . . . . . . . . . . . .  bahwa secara internal        11 12 13 14 15
            . . . . . . . . . . . . . . .  sel-sel disimpan dengan  =>  10 11 12 13 14
            [2,0] [2,1] [2,2] . . . [2,y]  barisan interger dimana      5  6  7  8  9
            [1,0] [1,1] [1,2] . . . [1,y]  kiri bawah adalah nol        0  1  2  3  4
            [0,0] [0,1] [0,2] . . . [0,y]          
                                 
            - board.states : dict -> Kondisi papan. 
            Key dari states adalah integer sel (0,1,..., x*y)
            Value adalah integer 1 atau 2:
            -> 1 artinya sudah diisi player 1
            -> 2 artinya sudah diisi player 2

            TODO: Tentukan x,y secara greedy. Kembalian adalah sebuah string "x,y"
            """
        best_move = "1,1"
        best_score = -1
        if (len(board.availables) == 64 or len(board.availables) == 63):
            if self.get_index(board, 3,3) not in board.states:
                return "3,3"
            else:
                return "4,4"

        for x in range(board.width):
            for y in range(board.height):
                index = self.get_index(board, x, y)
                if index not in board.states:
                    # print("OK: {} {} index: {}".format(x,y, index))
                    score = self.calculate_move_score(board, x, y)
                    # print("POINT: {} {}, SCORE : {}".format(x, y, score))
                    if score > best_score:
                        # print("BESTT POINT: {} {}, SCORE : {}".format(x, y, score))
                        best_move =  "{},{}".format(x, y)
                        best_score = score
                else:
                    # print("NOT OK")
                    continue
        # print(" END ")
        # print(best_move)
        return best_move
    
    def calculate_move_score(self, board, x, y):
        player = self.player 
        winning_score = 1000
        blocking_score = 800
        moving_towards_win_score = 600
        useless_win_score = 400

        # Check if the move leads to a winning position for the current player
        if self.is_winning_move(board, x, y, player):
            return winning_score

        # Check if the move blocks the opponent's winning position
        opponent = 2 if player == 1 else 1
        if self.is_winning_move(board, x, y, opponent):
            return blocking_score

        # Check if the move helps in moving towards a win
        move_score = 0
        move_score += self.count_adjacent_pieces(board, x, y, player, 1)  # Horizontal
        move_score += self.count_adjacent_pieces(board, x, y, player, -1)  # Reverse horizontal
        move_score += self.count_adjacent_pieces(board, x, y, player, 2)  # Vertical
        move_score += self.count_adjacent_pieces(board, x, y, player, -2)  # Reverse vertical
        move_score += self.count_adjacent_pieces(board, x, y, player, 3) * 1.01  # Diagonal \
        move_score += self.count_adjacent_pieces(board, x, y, player, -3) * 1.01 # Reverse diagonal \
        if move_score > 0:
            # Moves closer to center are preferred
            move_score += board.width + board.height
            return moving_towards_win_score + move_score

        # Return a lower score for moves that do not contribute to an eventual win
        return useless_win_score

    def is_winning_move(self, board, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Horizontal, Vertical, Diagonal (\), Reverse Diagonal (/)
    
        for dx, dy in directions:
            count = 1
            count += self.count_direction(board, x, y, player, dx, dy)  # Forward direction
            count += self.count_direction(board, x, y, player, -dx, -dy)  # Reverse direction
    
            if count >= 4:
                return True
    
        return False
    
    def count_adjacent_pieces(self, board, x, y, player, direction):
        directions = {
            1: (0, 1),    # Horizontal
            -1: (0, -1),  # Reverse horizontal
            2: (1, 0),    # Vertical
            -2: (-1, 0),  # Reverse vertical
            3: (1, 1),    # Diagonal \
            -3: (-1, -1)  # Reverse diagonal /
        }
        dx, dy = directions[direction]
        return self.count_direction(board, x, y, player, dx, dy)
    
    def count_direction(self, board, x, y, player, dx, dy):
        count = 0
        new_x, new_y = x + dx, y + dy
        while self.is_valid_position(board, new_x, new_y):
            if self.get_index(board, new_x, new_y) in board.states:
                if board.states[self.get_index(board, new_x, new_y)] == player:
                    count += 1
                    new_x += dx
                    new_y += dy
                else:
                    break
            else:
                break
        return count

    def is_valid_position(self, board, x, y):
        return 0 <= x < board.height and 0 <= y < board.width
    
    def get_index(self, board, x, y):
        return x * board.height + y
    

    def is_valid_index(self, pos):
        return pos >= 0 and pos <= 63
    