import random
import time
from enum import Enum


class Player(Enum):
    P1 = 1
    P2 = 2

class PIECE_COLOR(Enum):
    WHITE = "W"
    BLACK = "B"

class ChessGame:
    def __init__(self,number_of_players):
        self.number_of_players = number_of_players
        self.current_player = Player.P1
        self.game_finished = False
        self.chess_board = [["WR","WH","WB","WQ","WK","WB","WH","WR"],
                            ["WP","WP","WP","WP","WP","WP","WP","WP"],
                            ["","","","","","","",""],
                            ["","","","","","","",""],
                            ["","","","","","","",""],
                            ["","","","","","","",""],
                            ["BP","BP","BP","BP","BP","BP","BP","BP"],
                            ["BR","BH","BB","BQ","BK","BB","BH","BR"]]

    def display_board(self):
        header = "\n     " + " ".join(f"{i:^2}" for i in range(8))
        print(header)
        print("---------------------------")
        for i, row in enumerate(self.chess_board):
            print(i, "|", " ".join(
                [f"\033[92m{piece}\033[0m" if piece.startswith('W') else f"\033[91m{piece}\033[0m" if piece else ".."
                 for piece in row]))
        print("\n")

    def move(self,start_row, start_col, end_row, end_col):
        if start_row > 8 or start_row < 0:
            return "Invalid Input, the end row is not there."
        if start_col > 8 or start_col < 0:
            return "Invalid Input, the start column is not there."
        if end_row > 8 or end_row < 0:
            return "Invalid Input, the end row is not there."
        if end_col > 8 or end_col < 0:
            return "Invalid Input, the end column is not there."

        source = self.chess_board[start_row][start_col]
        destination = self.chess_board[end_row][end_col]

        if not source:
            return "There is no piece at the position."

        source_color = source[0]
        if self.current_player == Player.P1 and source_color == PIECE_COLOR.BLACK:
            return "You can't move up this piece, it is not on your team."
        if self.current_player == Player.P2 and source_color == PIECE_COLOR.WHITE:
            return "You can't move up this piece, it is not on your team."

        if destination:
            destination_color = destination[0]
            if destination_color == source_color:
                return "You cannot capture your own piece."

        if not self.valid_moves(start_row,start_col,end_row,end_col):
            return "Invalid Move"

        self.chess_board[end_row][end_col] = source
        self.chess_board[start_row][start_col] = ""

        if destination and 'K' in destination:
            self.game_finished = True
        else:
            if self.current_player == Player.P1:
                self.current_player = Player.P2
            else:
                self.current_player = Player.P1

    def valid_moves(self,start_row,start_col,end_row,end_col):
        piece = self.chess_board[start_row][start_col]
        capture_piece = self.chess_board[end_row][end_col]

        row_difference = abs(start_row - end_row)
        col_difference = abs(start_col - end_col)
        player_color = PIECE_COLOR.WHITE if self.current_player == Player.P1 else PIECE_COLOR.BLACK
        direction = 0

        match piece[1]:
            case 'K': #King
                return row_difference <= 1 and col_difference <= 1
            case 'R': #rook
                if start_row == end_row:
                    step = 1 if end_col > start_col else -1
                    for i in range(start_col + step, end_col, step):
                        if self.chess_board[start_row][i]:
                            return False
                    return True

                elif start_col == end_col:
                    step = 1 if end_row > start_row else -1
                    for i in range(start_row + step, end_row, step):
                        if self.chess_board[i][start_col]:
                            return False
                    return True
                return False
            case 'B': #bishop
                if row_difference == col_difference:
                    col_step = 1 if end_col > start_col else -1
                    row_step = 1 if end_row > start_row else -1
                    for i in range(1,col_difference):
                        if self.chess_board[start_row + i * row_step][start_col + i * col_step]:
                            return False
                    return True
                return False

            case 'H': #knight
                return (row_difference == 1 and col_difference == 2) or (col_difference == 1 and row_difference == 2)
            case 'Q': #queen
                if start_row == end_row:
                    step = 1 if end_col > start_col else -1
                    for i in range(start_col + step, end_col, step):
                        if self.chess_board[start_row][i]:
                            return False
                    return True

                elif start_col == end_col:
                    step = 1 if end_row > start_row else -1
                    for i in range(start_row + step, end_row, step):
                        if self.chess_board[i][start_col]:
                            return False
                    return True

                elif row_difference == col_difference:
                    col_step = 1 if end_col > start_col else -1
                    row_step = 1 if end_row > start_row else -1
                    for i in range(1,col_difference):
                        if self.chess_board[start_row + i * row_step][start_col + i * col_step]:
                            return False
                    return True
                return False
            case 'P': #pawn
                if piece[0] == "W":
                    direction = 1
                else:
                    direction = -1

                if not capture_piece:
                    return (start_col == end_col) and (end_row - start_row) == direction
                else:
                    return col_difference == 1 and (end_row - start_row) == direction


        return False

    def play(self):
        while not self.game_finished:
            self.display_board()
            time.sleep(4)
            if self.number_of_players == 1:
                self.play_with_comp()
            elif self.number_of_players == 2:
                self.play_with_opp()
            elif self.number_of_players == 3:
                self.play_with_ai_with_ai()
            else:
                return False

    def play_with_ai_with_ai(self):
        self.play_with_comp_advanced()
        pass

    def play_with_comp_advanced(self):
        piece_value = {"K" : 100, "Q" : 9, "R" : 5, "B" : 3, "H" : 3, "P" : 1}
        current_color = PIECE_COLOR.BLACK.value if self.current_player == Player.P2 else PIECE_COLOR.WHITE.value
        is_white = self.current_player == Player.P1
        best_score = -1
        best_capture = None
        empty_spaces = []
        low_priority_moves = []
        for r in range(8):
            for c in range(8):
                piece = self.chess_board[r][c]
                if piece and piece[0] == current_color:
                    for r2 in range(8):
                        for c2 in range(8):
                            target = self.chess_board[r2][c2]
                            if self.valid_moves(r,c,r2,c2):
                                if target and target[0] != current_color:
                                    score = piece_value.get(target[1],0)
                                    if score > best_score:
                                        best_score = score
                                        best_capture = (r,c,r2,c2)
                                else:
                                    if (is_white and r2 > r) or (not is_white and r2 < r):
                                        empty_spaces.append((r,c,r2,c2))
                                    else:
                                        low_priority_moves.append((r,c,r2,c2))

        if best_capture:
            self.move(*best_capture)
        elif len(empty_spaces) > 0:
            random_move = random.choice(empty_spaces)
            self.move(*random_move)
        else:
            low_priority_random_move = random.choice(low_priority_moves)
            self.move(*low_priority_random_move)

    def play_with_comp(self):
        if self.current_player == Player.P1:
            player_move = input("White Player enter the start row, start column, end row and end column | Use a comma to separate the values : ")
            try:
                start_row, start_col, end_row, end_col = map(int, player_move.split(","))
                result = self.move(start_row, start_col, end_row, end_col)
                print(result)
            except Exception as e:
                print(e)
        else:
            self.play_with_comp_advanced()
            # valid_moves = [(r,c,r2,c2) for r in range(8) for c in range(8) for r2 in range(8) for c2 in range(8) if self.chess_board[r][c] and self.chess_board[r][c][0] == "B" and self.valid_moves(r,c,r2,c2)]
            # print(valid_moves)
            # if valid_moves:
            #     move = random.choice(valid_moves)
            #     result = self.move(*move)
            #     print(result)

    def play_with_opp(self):
        if self.current_player == Player.P1:
            player_move = input("White Player enter the start row, start column, end row and end column | Use a comma to separate the values : ")
        else:
            player_move = input("Black Player enter the start row, start column, end row and end column | Use a comma to separate the values : ")
        try:
           start_row,start_col, end_row, end_col = map(int,player_move.split(","))
           result = self.move(start_row, start_col, end_row, end_col)
           print(result)
        except Exception as e:
            print(e)

    def getGameStatus(self):
        if self.game_finished:
            if self.current_player == Player.P1:
                return 1
            else:
                return 2
        else:
            return 0

    def getNextTurn(self):
        if self.game_finished:
            return -1
        return 1 if self.current_player == Player.P1 else 0

def main():
    print("Enter 1 if you want to play against a computer, enter 2 if you want to play against your friend or enter 3 if you want Ai vs Ai...")
    number_of_players = int(input("Enter the number of players : "))
    game = ChessGame(number_of_players)
    game.play()


if __name__ == "__main__":
    main()

