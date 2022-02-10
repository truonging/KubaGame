# Author: Ryan Truong
# Date: 2/5/22
# Description: Kuba board game where two players take turns moving their own marble L,R,F,B and the first person to
# push off all opponent marbles or captures 7 red marbles will win the game. The player can only move their own color
# marble, cant push off their own marble, and can not undo a move. If there is no room to move the marble, then player
# cant move that marble. Any player can start the game first.

import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 7, 7
SQUARE_SIZE = WIDTH//COLS  # how big the square is
FPS = 60
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (211, 211, 211)

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color, player=None):
        self.row = row
        self.col = col
        self.color = color
        self.player = player

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, BLACK, (self.x, self.y), radius + self.OUTLINE)  # draw bigger circle
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)  # draw smaller circle

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        if self.color == (255, 255, 255):
            return "[W]"
        if self.color == (0, 0, 0):
            return "[B]"
        if self.color == (255, 0, 0):
            return "[R]"


class KubaGame:
    """KubaGame class that initializes with a board and players. Methods to get turn,winner,marbles and make a move on a
    marble"""
    def __init__(self):
        """initializes with a 7x7 board, 8 white/black marbles, 13 red marbles. Unpacks two tuples as player,color.
        Set turn and winner to None, and set both points = 0"""
        # player 1 is white
        # player 2 is black
        self.player1, self.colorA = ('PlayerA', 'W')
        self.player2, self.colorB = ('PlayerB', 'B')
        self.board = [
            ["[W]", "[W]", "[ ]", "[ ]", "[ ]", "[B]", "[B]"],
            ["[W]", "[W]", "[ ]", "[R]", "[ ]", "[B]", "[B]"],
            ["[ ]", "[ ]", "[R]", "[R]", "[R]", "[ ]", "[ ]"],
            ["[ ]", "[R]", "[R]", "[R]", "[R]", "[R]", "[ ]"],
            ["[ ]", "[ ]", "[R]", "[R]", "[R]", "[ ]", "[ ]"],
            ["[B]", "[B]", "[ ]", "[R]", "[ ]", "[W]", "[W]"],
            ["[B]", "[B]", "[ ]", "[ ]", "[ ]", "[W]", "[W]"],
        ]
        self.other_board = []
        self.create_board()
        self.current_turn = self.player1
        self.player1_points = 0
        self.player2_points = 0
        self.winner = None
        self.selected_piece = None
        return

    def set_turn(self, player):
        """Method to set turn based on the player making the move"""
        if player is self.player1:              # if player1, then its player2 turn
            self.current_turn = self.player2
            return
        if player is self.player2:
            self.current_turn = self.player1    # if player2, then its player1 turn
            return

    def get_current_turn(self):
        """Returns current turn"""
        return self.current_turn

    def set_winner(self, player):
        """Set the winner depending on who made the move"""
        self.winner = player

    def get_winner(self):
        """Return the winner"""
        return self.winner

    def get_captured(self, player):
        """Return how many points the player has"""
        if player is self.player1:          # if player1, return player1 points
            return self.player1_points
        if player is self.player2:          # if player2, return player2 points
            return self.player2_points
        else:
            return "invalid player"

    def print_board(self):
        """Method to test board for testing purposes"""
        for row in self.board:
            print(*row)
        print("")
        return

    def get_marble(self, coords):
        """Method to return the whatever marble is in coords."""
        row, column = coords
        if not 0 <= row <= 6 or not 0 <= column <= 6:   # if value in row or column is not valid
            return
        if self.board[row][column] == "[ ]":            # if the tile is empty
            return "X"
        elif self.board[row][column] == "[W]":
            return "W"
        elif self.board[row][column] == "[B]":
            return "B"
        elif self.board[row][column] == "[R]":
            return "R"

    def get_marble_count(self):
        """Method to get total marble count and returns a tuple of those counts"""
        W = 0
        B = 0
        R = 0
        for row in self.board:
            for tile in row:
                if tile == "[W]":
                    W += 1
                elif tile == "[B]":
                    B += 1
                elif tile == "[R]":
                    R += 1
        counts = (W, B, R)
        return counts

    def check_winner(self, player):
        """Method to check for winner whether no opposing marbles left or player captured 7 red marbles"""
        # check if game ends by pushing all opposing marbles off
        # (W, B, R)
        if player is self.player1:  # if player1 and no more black marbles, player1 win
            if self.get_marble_count()[1] == 0:
                print(f"{player} has won the game by pushing off all opponent marbles!!")
                self.set_winner(player)
                return
        if player is self.player2:  # if player2 and no more white marbles, player2 win
            if self.get_marble_count()[0] == 0:
                print(f"{player} has won the game by pushing off all opponent marbles!!")
                self.set_winner(player)
                return
        # check if game ends by capturing 7 red marbles
        if self.get_captured(player) == 7:
            print(f"{player} has won the game by capturing 7 reds!!")
            self.set_winner(player)
            return

    def validate_move(self, player, row, column, direction):
        if self.get_winner() is not None:               # if game already decided
            print(f"Stop playing!! {self.get_winner()} has already won the game!!!")
            return False
        if not 0 <= row <= 6 or not 0 <= column <= 6:   # if value in row or column is not valid
            print("invalid numbers")
            return False
        if not self.validate_player(player, row, column):
            return False
        return True

    def validate_player(self, player, row, column):
        if self.board[row][column] == "[W]":            # if marble is not the players marble
            if player is self.player2:
                print("Cant move opponent marble")
                return False
        if self.board[row][column] == "[B]":            # if marble is not the players marble
            if player is self.player1:
                print("Cant move opponent marble")
                return False
        if self.board[row][column] == "[R]":            # if trying to move a red marble
            print("Cant move red marble")
            return False
        if self.board[row][column] == "[ ]":  # if player wants to move a tile at location but it empty
            print("Cant move empty tile")
            return False
        return True

    def move_right(self, player, row, column, direction):
        if self.board[row][column - 1] in ("[W]", "[B]", "[R]") and column != 0:  # if there is a marble to the left
            print("False move, no room to move marble")  # unless its the edge marble
            return False
        pos = 1
        pos2 = 0
        for tile in self.board[row][column:]:  # row but only starting FROM the tile in play
            if pos2 == len(self.board[row][column:]) - 1:  # if no empty tiles left to push, push off a marble
                if self.board[row][-1] == "[W]" and player is self.player1:  # if last marble is the players marble
                    print("False Move, cant push off own marble")
                    print("")
                    return False
                if self.board[row][-1] == "[B]" and player is self.player2:  # if last marble is the players marble
                    print("False Move, cant push off own marble")
                    print("")
                    return False
                temp_row = self.board[row][column:]  # make a temp row to shift values
                temp_row.insert(0, temp_row.pop())  # shift values right
                if temp_row[0] == "[R]":  # if marble pushed off is red
                    if player is self.player1:
                        self.player1_points += 1
                    if player is self.player2:
                        self.player2_points += 1
                    print(f"A red marble has been captured by {player}")
                temp_row[0] = "[ ]"  # delete marble that was pushed
                self.board[row][column:] = temp_row  # place back into the row the new values

                self.update_board()

                print(f"valid move done by {player}")
                print("")
                self.set_turn(player)  # if player1, then its player2. If player2, then its player1
                self.check_winner(player)  # checks whether move made by player made them win or not
                return True  # if so, set winner to player
            if tile == "[ ]":  # count how many pos it takes til empty tile
                break
            pos += 1
            pos2 += 1
        temp_row = self.board[row][column:column + pos]  # make a temp row to shift values
        temp_row.insert(0, temp_row.pop())  # shift values right
        self.board[row][column:column + pos] = temp_row  # place new shifted values back into row

        self.update_board()

        print(f"valid move done by {player}")
        print("")
        self.set_turn(player)
        return True

    def move_left(self, player, row, column, direction):
        if column != 6 and self.board[row][column + 1] in ("[W]", "[B]", "[R]"):  # if there is a marble to the right
            print("False move, no room to move marble")  # unless its the edge marble
            return False
        pos = 1
        pos2 = 0
        for tile in self.board[row][column::-1]:  # row but only starting FROM the tile in play
            if pos2 == len(self.board[row][column::-1]) - 1:  # if not tiles left to push, push off a marble
                if self.board[row][0] == "[W]" and player is self.player1:  # if last marble is the player's marble
                    print("False Move, cant push off own marble \n")
                    return False
                if self.board[row][0] == "[B]" and player is self.player2:  # if last marble is the player's marble
                    print("False Move, cant push off own marble \n")
                    return False
                temp_row = self.board[row][column::-1]  # make a temp row to shift values
                temp_row.insert(0, temp_row.pop())  # shift values right
                if temp_row[0] == "[R]":  # if marble pushed off is red
                    if player is self.player1:  # if marble pushed off is red
                        self.player1_points += 1
                    if player is self.player2:
                        self.player2_points += 1
                    print(f"A red marble has been captured by {player}")
                temp_row[0] = "[ ]"  # delete last marble that was pushed
                self.board[row][column::-1] = temp_row  # while reading backwards place new values in row

                self.update_board()

                print(f"valid move done by {player} \n")
                self.set_turn(player)  # if player1, then its player2. If player2, then its player1
                self.check_winner(player)  # checks whether move made by player made them win or not
                return True  # if so, set winner to player
            if tile == "[ ]":  # count how many pos it takes til empty tile
                break
            pos += 1
            pos2 += 1
        temp_row = self.board[row][column:column - pos:-1]  # make a temp row to shift values
        temp_row.insert(0, temp_row.pop())  # shift values right
        self.board[row][column:column - pos:-1] = temp_row  # while reading backwards, place new values in row

        self.update_board()

        print(f"valid move done by {player} \n")
        self.set_turn(player)
        return True

    def move_forward(self, player, row, column, direction):
        if row != 6 and self.board[row + 1][column] in ("[W]", "[B]", "[R]"):  # if there is a marble one row in front
            print("False move, no room to move marble \n")  # unless its the edge marble
            return False
        pos = 1
        pos2 = 0
        for rows in self.board[row::-1]:  # count how many rows it takes to reach an empty tile
            if pos == len(self.board[row::-1]):  # if no empty tiles left to push, push off marble
                if self.board[row - pos2::-1][0][column] == "[W]" and player is self.player1:
                    print("False move, cant push off own marble \n")  # if last marble is the players marble
                    return False
                if self.board[row - pos2::-1][0][column] == "[B]" and player is self.player2:
                    print("False move, cant push off own marble \n")  # if last marble is the players marble
                    return False
                while pos2 != 0:
                    # whichever tile is on the last row, switch that tile with the tile behind it until it reaches
                    # the initial row that the player chose
                    self.board[row - pos2::-1][0].insert(column, self.board[row - pos2 + 1::-1][0].pop(column))
                    self.board[row - pos2 + 1::-1][0].insert(column, self.board[row - pos2::-1][0].pop(column + 1))
                    pos2 -= 1
                if self.board[row - pos2::-1][0][column] == "[R]":  # if last marble being pushed off is red
                    if player is self.player1:
                        self.player1_points += 1
                    if player is self.player2:
                        self.player2_points += 1
                    print(f"A red marble has been captured by {player}")
                self.board[row - pos2::-1][0][column] = "[ ]"  # delete last marble that was pushed

                self.update_board()

                print(f"valid move done by {player} \n")
                self.set_turn(player)  # if player1, then its player2. If player2, then its player1
                self.check_winner(player)  # checks whether move made by player made them win or not
                return True  # if so, set winner to player
            if rows[column] == "[ ]":
                break
            pos += 1
            pos2 += 1
        while pos2 != 0:
            # while reading backwards, insert into the row that contains the empty tile, the tile in the row behind it
            # (technically the row in front, but we reading backwards) then insert in the row we just popped a val from,
            # the empty tile that we are switching.
            # Repeat until the empty tile reaches the initial row that the player chose
            self.board[row::-1][pos2].insert(column, self.board[row::-1][pos2 - 1].pop(column))
            self.board[row::-1][pos2 - 1].insert(column, self.board[row::-1][pos2].pop(column + 1))
            pos2 -= 1

        self.update_board()

        print(f"valid move done by {player} \n")
        self.set_turn(player)
        return True

    def move_back(self, player, row, column, direction):
        if row != 0 and self.board[row - 1][column] in ("[W]", "[B]", "[R]"):  # if there is a marble one row behind
            print("False move, no room to move marble \n")  # unless its a edge marble
            return False
        pos = 1
        pos2 = 0
        for rows in self.board[row::]:  # count how many rows it takes to reach an empty tile
            if pos == len(self.board[row::]):  # if no empty tile left to push, push off marble
                if self.board[row + pos2::][0][column] == "[W]" and player is self.player1:
                    print("False move, cant push off own marble \n")  # if last marble is the players marble
                    return False
                if self.board[row + pos2::][0][column] == "[B]" and player is self.player2:
                    print("False move, cant push off own marble \n")  # if last marble is the players marble
                    return False
                while pos2 != 0:
                    # whichever tile is in the last row, switch that tile with the tile behind it until it reaches
                    # the initial row that the player chose
                    self.board[row::][pos2].insert(column, self.board[row::][pos2 - 1].pop(column))
                    self.board[row::][pos2 - 1].insert(column, self.board[row::][pos2].pop(column + 1))
                    pos2 -= 1
                if self.board[row::][0][column] == "[R]":  # if last marble being pushed off is red
                    if player is self.player1:
                        self.player1_points += 1
                    if player is self.player2:
                        self.player2_points += 1
                    print(f"A red marble has been captures by {player}")
                self.board[row::][0][column] = "[ ]"  # delete the marble being pushed off

                self.update_board()

                print(f"valid move done by {player} \n")
                self.set_turn(player)  # if player1, then its player2. If player2, then its player1
                self.check_winner(player)  # checks whether move made by player made them win or not
                return True  # if so, set winner to player
            if rows[column] == "[ ]":
                break
            pos += 1
            pos2 += 1
        while pos2 != 0:
            # starting with the empty tile in the first row iterated that contained an empty tile, switch
            # that empty tile with the tile, one row behind it. Repeat until the empty tile reaches the initial
            # row the player chose
            self.board[row::][pos2].insert(column, self.board[row::][pos2 - 1].pop(column))
            self.board[row::][pos2 - 1].insert(column, self.board[row::][pos2].pop(column + 1))
            pos2 -= 1

        self.update_board()

        print(f"valid move done by {player} \n")
        self.set_turn(player)
        return True

    def make_move(self, player, coords, direction):
        """make_move method that first checks if move can be validated before checking which direction to go taking
        player, coords, and direction as parameters, returning False if the move cant be made and True if successful"""
        row, column = coords
        if not self.validate_move(player, row, column, direction):
            return False

        if direction == "R":      # go right
            if not self.move_right(player, row, column, direction):
                return False

        if direction == "L":      # go left
            if not self.move_left(player, row, column, direction):
                return False

        if direction == "F":
            if not self.move_forward(player, row, column, direction):
                return False

        if direction == "B":
            if not self.move_back(player, row, column, direction):
                return False
        return

    def draw_squares(self, win):
        win.fill(GRAY)

        for row in range(0, WIDTH, SQUARE_SIZE):
            for col in range(0, HEIGHT, SQUARE_SIZE):
                rect = pygame.Rect(row, col, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(win, BLACK, rect, 1)

    def create_board(self):
        for row in range(ROWS):
            self.other_board.append([])
            for col in range(COLS):
                if self.board[row][col] == "[W]":
                    self.other_board[row].append(Piece(row, col, WHITE, 'PlayerA'))
                elif self.board[row][col] == "[B]":
                    self.other_board[row].append(Piece(row, col, BLACK, 'PlayerB'))
                elif self.board[row][col] == "[R]":
                    self.other_board[row].append(Piece(row, col, RED))
                else:
                    self.other_board[row].append("[ ]")

    def update_board(self):
        self.other_board = []
        for row in range(ROWS):
            self.other_board.append([])
            for col in range(COLS):
                if self.board[row][col] == "[W]":
                    self.other_board[row].append(Piece(row, col, WHITE, 'PlayerA'))
                elif self.board[row][col] == "[B]":
                    self.other_board[row].append(Piece(row, col, BLACK, 'PlayerB'))
                elif self.board[row][col] == "[R]":
                    self.other_board[row].append(Piece(row, col, RED))
                else:
                    self.other_board[row].append("[ ]")

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.other_board[row][col]
                if piece != "[ ]":
                    piece.draw(win)

    def update(self):
        self.draw(WIN)
        pygame.display.update()

    def get_piece(self, row, col):
        return self.other_board[row][col]

    def select(self, row, col):
        if self.get_winner() is not None:
            print(f"Stop playing!! {self.get_winner()} has already won the game!!!")
            return False
        piece = self.get_piece(row, col)
        if piece != "[ ]" and piece.player == self.current_turn:
            self.selected_piece = (row, col)
            print(f"Selected correctly {self.selected_piece}")
            return True
        self.validate_player(self.get_current_turn(), row, col)
        return False

    def set_direction(self, direction):
        if self.get_winner() is not None:
            print(f"Stop playing!! {self.get_winner()} has already won the game!!!")
        if self.selected_piece:
            self.make_move(self.get_current_turn(), self.selected_piece, direction)
            self.selected_piece = None

    def show_score(self, x, y):
        score1 = font.render("White Score : " + str(self.player1_points), True, BLUE)
        score2 = font.render("Black Score : " + str(self.player2_points), True, BLUE)
        WIN.blit(score1, (x, y))
        WIN.blit(score2, (x+620, y))


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


pygame.init()
font = pygame.font.Font(None, 32)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kuba")


def main():
    run = True
    clock = pygame.time.Clock()
    game = KubaGame()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.set_direction("R")
                if event.key == pygame.K_LEFT:
                    game.set_direction("L")
                if event.key == pygame.K_UP:
                    game.set_direction("F")
                if event.key == pygame.K_DOWN:
                    game.set_direction("B")

        game.draw(WIN)
        game.show_score(10, 0)
        pygame.display.update()

    pygame.quit()


main()


"""
game = KubaGame()
game.make_move('PlayerA', (1, 0), 'R')
game.print_board()
game.make_move('PlayerB', (6, 1), 'F')
game.print_board()
game.make_move('PlayerA', (1, 6), 'L')
game.make_move('PlayerA', (5, 6), 'L')
game.print_board()
"""
