import pygame
import time
import sys

class Game(object):
    # game object
    def __init__(self, screen, chessboard):
        self.screen = screen
        self.player = "r"
        # place the image
        self.player_tips_r_image = pygame.image.load("images/red.png")
        self.player_tips_r_image_topleft = (500, 500)
        self.player_tips_b_image = pygame.image.load("images/black.png")
        self.player_tips_b_image_topleft = (500, 100)

        self.show_attack = False
        self.show_attack_count = 0
        self.show_attack_time = 100
        self.attack_img = pygame.image.load("images/pk.png")
        self.show_win = False
        self.win_img = pygame.image.load("images/win.png")
        self.win_player = None
        self.show_win_count = 0
        self.show_win_time = 300
        self.chessboard = chessboard

    def get_player(self):
        # get the current player
        return self.player

    def exchange(self):
        # exchange the player
        self.player = "r" if self.player == "b" else "b"
        return self.get_player()

    def reset_game(self):
        # reset the game
        self.chessboard.create_chess()
        self.player = 'r'

    def show(self):
        # if one side win, then show "Win" image
        if self.show_win:
            self.show_win_count += 1
            if self.show_win_count == self.show_win_time:
                self.show_win_count = 0
                self.show_win = False
                self.reset_game()

        if self.show_win:
            if self.win_player == "b":
                self.screen.blit(self.win_img, (550, 100))
            else:
                self.screen.blit(self.win_img, (550, 450))
            return

        # set the time the "general" will show
        if self.show_attack:
            self.show_attack_count += 1
            if self.show_attack_count == self.show_attack_time:
                self.show_attack_count = 0
                self.show_attack = False

        if self.player == "r":
            self.screen.blit(self.player_tips_r_image, self.player_tips_r_image_topleft)
            # show "general" image
            if self.show_attack:
                self.screen.blit(self.attack_img, (230, 400))
        else:
            # show "general" image
            if self.show_attack:
                self.screen.blit(self.attack_img, (230, 100))
            self.screen.blit(self.player_tips_b_image, self.player_tips_b_image_topleft)

    def set_attack(self):
        self.show_attack = True

    def set_win(self, win_player):
        # set the winner
        self.show_win = True
        self.win_player = win_player

class Dot(object):
    # I will use this object to store all the references of "position can be moved"
    group = list()

    def __init__(self, screen, row, col):
        # initial
        self.image = pygame.image.load("images/dot2.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (60 + col * 57, 60 + row * 57)
        self.screen = screen
        self.row = row
        self.col = col

    def show(self):
        # show the chess
        self.screen.blit(self.image, self.rect.topleft)

    @classmethod
    def create_nums_dot(cls, screen, pos_list):
        # create objects in batches
        for temp in pos_list:
            cls.group.append(cls(screen, *temp))

    @classmethod
    def clean_last_position(cls):
        # clear all the Dot object
        cls.group.clear()

    @classmethod
    def show_all(cls):
        for temp in cls.group:
            temp.show()

    @classmethod
    def click(cls):
        # when the place can be moved is clicked, print the information
        for dot in cls.group:
            if pygame.mouse.get_pressed()[0] and dot.rect.collidepoint(pygame.mouse.get_pos()):
                print("the place can be moved is clicked.")
                return dot


class ClickBox(pygame.sprite.Sprite):
    singleton = None
    # show the click

    def __new__(cls, *args, **kwargs):
        # rewrite the object to make sure there is only one for this object
        if cls.singleton is None:
            cls.singleton = super().__new__(cls)
        return cls.singleton

    def __init__(self, screen, row, col):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("images/r_box.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (50 + col * 57, 50 + row * 57)
        self.row = row
        self.col = col

    @classmethod
    def show(cls):
        if cls.singleton:
            cls.singleton.screen.blit(cls.singleton.image, cls.singleton.rect)

    @classmethod
    def clean(cls):
        # clear the previous object
        cls.singleton = None

class Chess(pygame.sprite.Sprite):
    # "chess class"
    def __init__(self, screen, chess_name, row, col):
        super().__init__()
        self.screen = screen
        self.team = chess_name[0]
        self.name = chess_name[2]
        self.image = pygame.image.load("images/" + chess_name + ".png")
        self.top_left = (50 + col * 57,50 + row * 57)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50 + col * 57, 50 + row * 57)
        self.row, self.col = row, col

    def show(self):
        # place the chess
        self.screen.blit(self.image, self.rect)

    @staticmethod
    # def get_clicked_chess(chessboard):
    def get_clicked_chess(player, chessboard):
        # get the chess be clicked
        for chess in chessboard.get_chess():
            if pygame.mouse.get_pressed()[0] and chess.rect.collidepoint(pygame.mouse.get_pos()):
                if player == chess.team:
                    print(chess.name + " be clicked")
                    return chess

    def update_position(self,new_row,new_col):
        # update the chess position after the chess be moved
        self.col = new_col
        self.row = new_row
        self.rect.topleft = (50 + new_col * 57,50 + new_row * 57)



class ChessBoard(object):
    # "create the chessboard"
    def __init__(self,screen):
        # "initial"
        self.screen = screen
        self.image = pygame.image.load("images/bg.png")
        self.topleft = (50, 50)
        self.chessboard_map = None
        self.create_chess()

    def show(self):
        # show the chessboard
        self.screen.blit(self.image,self.topleft)

    def create_chess(self):
        self.chessboard_map = [
            ["b_c", "b_m", "b_x", "b_s", "b_j", "b_s", "b_x", "b_m", "b_c"],
            ["", "", "", "", "", "", "", "", ""],
            ["", "b_p", "", "", "", "", "", "b_p", ""],
            ["b_z", "", "b_z", "", "b_z", "", "b_z", "", "b_z"],
            ["", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", ""],
            ["r_z", "", "r_z", "", "r_z", "", "r_z", "", "r_z"],
            ["", "r_p", "", "", "", "", "", "r_p", ""],
            ["", "", "", "", "", "", "", "", ""],
            ["r_c", "r_m", "r_x", "r_s", "r_j", "r_s", "r_x", "r_m", "r_c"],
        ]

        for row, line in enumerate(self.chessboard_map):
            for col, chess_name in enumerate(line):
                if chess_name:
                    self.chessboard_map[row][col] = Chess(self.screen, chess_name, row, col)
                else:
                    self.chessboard_map[row][col] = None

    def show_chess(self):
        # show all the chess on the chessboard
        for chess_line in self.chessboard_map:
            for chess in chess_line:
                if chess:
                    chess.show()

    def show_chessboard_and_chess(self):
        self.show()
        self.show_chess()

    def get_chess(self):
        # return all the chess on the chess board
        return [chess for chessline in self.chessboard_map for chess in chessline if chess]

    def get_put_down_postion(self, clicked_chess):
        # get the position the chess can put down
        put_down_chess_pos = list()
        team = clicked_chess.team
        row = clicked_chess.row
        col = clicked_chess.col
        map_ = self.chessboard_map

        if clicked_chess.name == 'z':
            # 兵
            if team == 'r': #red side
                if row - 1 >= 0:
                    if not map_[row - 1][col] or map_[row - 1][col].team != team:
                        put_down_chess_pos.append((row - 1,col))
            else: #black side
                if row + 1 <= 9:
                    if not map_[row + 1][col] or map_[row + 1][col].team != team:
                        put_down_chess_pos.append((row + 1, col))

            # judge the direction
            if (team == 'r' and 0 <= row <= 4) or (team == 'b' and 5 <= row <= 9):
                # left
                if col - 1 >= 0 and (not map_[row][col - 1] or map_[row][col - 1].team != team):
                    put_down_chess_pos.append((row, col - 1))
                # right
                if col + 1 <= 8 and (not map_[row][col + 1] or map_[row][col + 1].team != team):
                    put_down_chess_pos.append((row, col + 1))
        elif clicked_chess.name == "j":
            #jiang jun
            row_start, row_stop = (0, 2) if team == "b" else (7, 9)
            # direction judgement
            if row - 1 >= row_start and (not map_[row - 1][col] or map_[row - 1][col].team != team):
                put_down_chess_pos.append((row - 1, col))
            if row + 1 <= row_stop and (not map_[row + 1][col] or map_[row + 1][col].team != team):
                put_down_chess_pos.append((row + 1, col))
            if col - 1 >= 3 and (not map_[row][col - 1] or map_[row][col - 1].team != team):
                put_down_chess_pos.append((row, col - 1))
            if col + 1 <= 5 and (not map_[row][col + 1] or map_[row][col + 1].team != team):
                put_down_chess_pos.append((row, col + 1))
        elif clicked_chess.name == "s":
            #shi
            row_start, row_stop = (0, 2) if team == "b" else (7, 9)
            # direction judgement
            if row - 1 >= row_start and col - 1 >= 3 and (not map_[row - 1][col - 1] or map_[row - 1][col - 1].team != team):
                put_down_chess_pos.append((row - 1, col - 1))
            if row - 1 >= row_start and col + 1 <= 5 and (not map_[row - 1][col + 1] or map_[row - 1][col + 1].team != team):
                put_down_chess_pos.append((row - 1, col + 1))
            if row + 1 <= row_stop and col - 1 >= 3 and (not map_[row + 1][col - 1] or map_[row + 1][col - 1].team != team):
                put_down_chess_pos.append((row + 1, col - 1))
            if row + 1 <= row_stop and col + 1 <= 5 and (not map_[row + 1][col + 1] or map_[row + 1][col + 1].team != team):
                put_down_chess_pos.append((row + 1, col + 1))

        elif clicked_chess.name == "x":
            # xiang
            row_start, row_stop = (0, 4) if team == "b" else (5, 9)
            #direction judgement
            #left top
            if row - 2 >= row_start and col - 2 >= 0 and (not map_[row - 2][col - 2] or map_[row - 2][col - 2].team != team):
                if not map_[row - 1][col - 1]:
                    put_down_chess_pos.append((row - 2, col - 2))
            #left down
            if row + 2 <= row_stop and col - 2 >= 0 and (not map_[row + 2][col - 2] or map_[row + 2][col - 2].team != team):
                if not map_[row + 1][col - 1]:
                    put_down_chess_pos.append((row + 2, col - 2))
            #right top
            if row - 2 >= row_start and col + 2 <= 8 and (not map_[row - 2][col + 2] or map_[row - 2][col + 2].team != team):
                if not map_[row - 1][col + 1]:
                    put_down_chess_pos.append((row - 2, col + 2))
            #right down
            if row + 2 <= row_stop and col + 2 <= 8 and (not map_[row + 2][col + 2] or map_[row + 2][col + 2].team != team):
                if not map_[row + 1][col + 1]:
                    put_down_chess_pos.append((row + 2, col + 2))

        elif clicked_chess.name == "m":
            #ma
            #direction judgement
            #竖日
            #left top
            if row - 2 >= 0 and col - 1 >= 0 and (not map_[row - 2][col - 1] or map_[row - 2][col - 1].team != team):
                if not map_[row - 1][col]:
                    put_down_chess_pos.append((row - 2, col - 1))
            #left down
            if row + 2 <= 9 and col - 1 >= 0 and (not map_[row + 2][col - 1] or map_[row + 2][col - 1].team != team):
                if not map_[row + 1][col]:
                    put_down_chess_pos.append((row + 2, col - 1))
            #right top
            if row - 2 >= 0 and col + 1 <= 8 and (not map_[row - 2][col + 1] or map_[row - 2][col + 1].team != team):
                if not map_[row - 1][col]:
                    put_down_chess_pos.append((row - 2, col + 1))
            #right down
            if row + 2 <= 9 and col + 1 <= 8 and (not map_[row + 2][col + 1] or map_[row + 2][col + 1].team != team):
                if not map_[row + 1][col]:
                    put_down_chess_pos.append((row + 2, col + 1))
            #横日
            # left top
            if row - 1 >= 0 and col - 2 >= 0 and (not map_[row - 1][col - 2] or map_[row - 1][col - 2].team != team):
                if not map_[row][col - 1]:
                    put_down_chess_pos.append((row - 1, col - 2))
            # left down
            if row + 1 <= 9 and col - 2 >= 0 and (not map_[row + 1][col - 2] or map_[row + 1][col - 2].team != team):
                if not map_[row][col - 1]:
                    put_down_chess_pos.append((row + 1, col - 2))
            # right top
            if row - 1 >= 0 and col + 2 >= 8 and (not map_[row - 1][col + 2] or map_[row - 1][col + 2].team != team):
                if not map_[row][col + 1]:
                    put_down_chess_pos.append((row - 1, col + 2))
            # right down
            if row + 1 <= 9 and col + 2 <= 8 and (not map_[row + 1][col + 2] or map_[row + 1][col + 2].team != team):
                if not map_[row][col + 1]:
                    put_down_chess_pos.append((row + 1, col + 2))

        elif clicked_chess.name == "c":
            #che
            #direction judgement
            #列
            up_set = False
            down_set = False
            for i in range(1, 10):
                if row + i <= 9 and not down_set:
                    if not map_[row + i][col]:
                        #if there is no other chess in this position
                        put_down_chess_pos.append((row + i,col))
                    elif map_[row + i][col].team != team:
                        put_down_chess_pos.append((row + i,col))
                        down_set = True
                    else:
                        down_set = True

                if row - i >= 0 and not up_set:
                    if not map_[row - i][col]:
                        #if there is no other chess in this position
                        put_down_chess_pos.append((row - i,col))
                    elif map_[row - i][col].team != team:
                        put_down_chess_pos.append((row - i,col))
                        up_set = True
                    else:
                        up_set = True

            #行
            left_set = False
            right_set = False
            for j in range(1, 9):
                if col + j <= 8 and not right_set:
                    if not map_[row][col + j]:
                        # if there is no other chess in this position
                        put_down_chess_pos.append((row, col + j))
                    elif map_[row][col + j].team != team:
                        put_down_chess_pos.append((row, col + j))
                        right_set = True
                    else:
                        right_set = True

                if col - j >= 0 and not left_set:
                    if not map_[row][col - j]:
                        # if there is no other chess in this position
                        put_down_chess_pos.append((row, col - j))
                    elif map_[row][col - j].team != team:
                        put_down_chess_pos.append((row, col - j))
                        left_set = True
                    else:
                        left_set = True

        elif clicked_chess.name == "p":
            #pao
            direction_left_chess_num = 0
            direction_right_chess_num = 0
            for i in range(1, 9):
                # 计算当前行中，棋子左边与右边可以落子的位置
                # 左边位置没有越界
                if direction_left_chess_num >= 0 and col - i >= 0:
                    if not map_[row][col - i] and direction_left_chess_num == 0:
                        # 如果没有棋子,则将当前位置组成一个元组，添加到列表
                        put_down_chess_pos.append((row, col - i))
                    elif map_[row][col - i]:
                        # 如果当前位置有棋子，那么就判断是否能够吃掉它
                        direction_left_chess_num += 1
                        if direction_left_chess_num == 2 and map_[row][col - i].team != team:
                            put_down_chess_pos.append((row, col - i))
                            direction_left_chess_num = -1  # 让其不能够在下次for循环时再次判断
                # 右边位置没有越界
                if direction_right_chess_num >= 0 and col + i <= 8:
                    if not map_[row][col + i] and direction_right_chess_num == 0:
                        # 如果没有棋子,则将当前位置组成一个元组，添加到列表
                        put_down_chess_pos.append((row, col + i))
                    elif map_[row][col + i]:
                        # 如果当前位置有棋子，那么就判断是否能够吃掉它
                        direction_right_chess_num += 1
                        if direction_right_chess_num == 2 and map_[row][col + i].team != team:
                            put_down_chess_pos.append((row, col + i))
                            direction_right_chess_num = -1
            # 一列
            direction_up_chess_num = 0
            direction_down_chess_num = 0
            for i in range(1, 10):  # 这样就让i从1开始，而不是从0
                # 计算当前列中，棋子上边与下边可以落子的位置
                # 上边位置没有越界
                if direction_up_chess_num >= 0 and row - i >= 0:
                    if not map_[row - i][col] and direction_up_chess_num == 0:
                        # 如果没有棋子,则将当前位置组成一个元组，添加到列表
                        put_down_chess_pos.append((row - i, col))
                    elif map_[row - i][col]:
                        # 如果当前位置有棋子，那么就判断是否能够吃掉它
                        direction_up_chess_num += 1
                        if direction_up_chess_num == 2 and map_[row - i][col].team != team:
                            put_down_chess_pos.append((row - i, col))
                            direction_up_chess_num = -1

                # 下边位置没有越界
                if direction_down_chess_num >= 0 and row + i <= 9:
                    if not map_[row + i][col] and direction_down_chess_num == 0:
                        # 如果没有棋子,则将当前位置组成一个元组，添加到列表
                        put_down_chess_pos.append((row + i, col))
                    elif map_[row + i][col]:
                        # 如果当前位置有棋子，那么就判断是否能够吃掉它
                        direction_down_chess_num += 1
                        if direction_down_chess_num == 2 and map_[row + i][col].team != team:
                            put_down_chess_pos.append((row + i, col))
                            direction_down_chess_num = -1


        return put_down_chess_pos

    def judge_delete_position(self, all_position, clicked_chess):
        deleting_position = list()

        # 判断这些位置，是否会导致被"将军"，如果是则从列表中删除这个位置
        for row, col in all_position:
            # 1. 备份
            # 备份当前棋子位置
            old_row, old_col = clicked_chess.row, clicked_chess.col
            # 备份要落子的位置的棋子(如果没有，则为None)
            position_chess_backup = self.chessboard_map[row][col]
            # 2. 挪动位置
            # 移动位置
            self.chessboard_map[row][col] = self.chessboard_map[old_row][old_col]
            # 修改棋子的属性
            self.chessboard_map[row][col].update_position(row, col)
            # 清楚之前位置为None
            self.chessboard_map[old_row][old_col] = None
            # 3. 判断对方是否可以发起"将军"
            if self.judge_attack_general("b" if clicked_chess.team == "r" else "r"):
                deleting_position.append((row, col))
            # 4. 恢复到之前位置
            self.chessboard_map[old_row][old_col] = self.chessboard_map[row][col]
            self.chessboard_map[old_row][old_col].update_position(old_row, old_col)
            self.chessboard_map[row][col] = position_chess_backup

        # 5. 删除不能落子的位置
        all_position = list(set(all_position) - set(deleting_position))

        return all_position

    def move_chess(self, new_row, new_col):
        # move the chess to the new position
        # first,get the old position of the chess
        old_row, old_col = ClickBox.singleton.row, ClickBox.singleton.col
        print("old position: ", old_row, old_col, "new position: ", new_row, new_col)
        self.chessboard_map[new_row][new_col] = self.chessboard_map[old_row][old_col]
        # modify the attribution of the chess
        self.chessboard_map[new_row][new_col].update_position(new_row,new_col)
        #clean the chess in old position
        self.chessboard_map[old_row][old_col] = None

    def get_general_position(self, general_player):
        for row, line in enumerate(self.chessboard_map):
            for col, chess in enumerate(line):
                if chess and chess.team == general_player and chess.name == "j":
                    return chess.row, chess.col

    def judge_j_attack(self, attack_row, attack_col, general_row, general_col):
        if attack_col == general_col:
            # two general in the same column
            min_row, max_row = (attack_row, general_row) if attack_row < general_row else (general_row, attack_row)

            chess_num = 0
            for i in range(min_row + 1, max_row):
                if self.chessboard_map[i][general_col]:
                    chess_num += 1

            if chess_num == 0:
                return True

    def judge_m_attack(self, attack_row, attack_col, general_row, general_col):
        # judge chess ma can attack the general
        if attack_col == general_col or attack_row == general_row:
            return False
        else:
            col_length = (attack_col - general_col) ** 2
            row_length = (attack_row - general_row) ** 2

            if col_length + row_length == 5:
                if col_length == 1:
                    if attack_row > general_row and not self.chessboard_map[attack_row - 1][attack_col]:
                        return True
                    elif attack_row < general_row and not self.chessboard_map[attack_row + 1][attack_col]:
                        return True
                elif col_length == 4:
                    if attack_col > general_col and not self.chessboard_map[attack_row][attack_col - 1]:
                        return True
                    elif attack_col < general_col and not self.chessboard_map[attack_row][attack_col + 1]:
                        return True

    def judge_c_and_p_attack(self, attack_chess_name, attack_row, attack_col, general_row, general_col):
        if attack_chess_name == "c":
            map_ = self.chessboard_map
            c_set = True
            num = 1
            if attack_row == general_row:
                # in the same row
                num -= 1
                min_start, max_stop = 0, 0
                if attack_col < general_row:
                    min_start, max_stop = (attack_col, general_col)
                else:
                    min_start, max_stop = (general_col, attack_col)
                length = max_stop - min_start
                for i in range(min_start + 1, max_stop):
                    if map_[attack_row][i] and map_[attack_row][i].name != "j":
                        c_set = False
            elif attack_col == general_col:
                # in the same col
                num -= 1
                min_start, max_stop = 0,0
                if attack_row < general_row:
                    min_start, max_stop = (attack_row, general_row)
                else:
                    min_start, max_stop = (general_row, attack_row)
                length = max_stop - min_start
                for i in range(min_start + 1, max_stop):
                    if map_[i][attack_col] and map_[i][attack_col].name != "j":
                        c_set = False

            if num == 1:
                return False

            return c_set

        elif attack_chess_name == "p":
            check_chess_num = 1
            chess_num = 0
            if attack_row == general_row:
                # 在同一行
                min_col, max_col = (attack_col, general_col) if attack_col < general_col else (general_col, attack_col)
                for i in range(min_col + 1, max_col):
                    if self.chessboard_map[attack_row][i]:
                        chess_num += 1
                if chess_num == check_chess_num:
                    return True
            elif attack_col == general_col:
                # 在同一列
                min_row, max_row = (attack_row, general_row) if attack_row < general_row else (general_row, attack_row)
                for i in range(min_row + 1, max_row):
                    if self.chessboard_map[i][general_col]:
                        chess_num += 1
                if chess_num == check_chess_num:
                    return True

    @staticmethod
    def judge_z_attack(attack_team, attack_row, attack_col, general_row, general_col):
        if attack_team == "r" and attack_row < general_row:
            return False
        elif attack_team == "b" and attack_row > general_row:
            return False
        elif (attack_row - general_row) ** 2 + (attack_col - general_col) ** 2 == 1:
            return True

    def judge_attack_general(self, attact_player):
        # first, get the position of general of another player
        if attact_player == "b":
            general_player = "r"
        else:
            general_player = "b"
        general_position = self.get_general_position(general_player)

        # second, traverse all the chess of mine
        for row, line in enumerate(self.chessboard_map):
            for col, chess in enumerate(line):
                if chess and chess.team == attact_player:
                    if chess.name == "z":  # 兵
                        # 传递5个参数（攻击方的标识，攻击方row，攻击方col，对方将row，对方将col）
                        if self.judge_z_attack(chess.team, chess.row, chess.col, *general_position):
                            return True
                    elif chess.name == "p":  # 炮
                        if self.judge_c_and_p_attack(chess.name, chess.row, chess.col, *general_position):
                            return True
                    elif chess.name == "c":  # 车
                        if self.judge_c_and_p_attack(chess.name, chess.row, chess.col, *general_position):
                            return True
                    elif chess.name == "m":  # 马
                        if self.judge_m_attack(chess.row, chess.col, *general_position):
                            return True
                    elif chess.name == "x":  # 象
                        pass
                    elif chess.name == "s":  # 士
                        pass
                    elif chess.name == "j":  # 将
                        if self.judge_j_attack(chess.row, chess.col, *general_position):
                            return True

    def judge_win(self, attack_player):
        # traverse all the chess for the attacked player, test if there is possible to block the attack
        for chess_line in self.chessboard_map:
            for chess in chess_line:
                if chess and chess.team != attack_player:
                    move_position_list = self.get_put_down_postion(chess)
                    if move_position_list:  # 只要找到一个可以移动的位置，就表示没有失败，还是有机会的
                        return False

        return True



def main():
    # initial pygame
    pygame.init()
    # create object to show the screen
    screen = pygame.display.set_mode((750, 667))
    # load background image
    background_img = pygame.image.load("images/bg.jpg")
    # chessboard
    # chessboard_img = pygame.image.load("images/bg.png")
    # create chessboard
    chessboard = ChessBoard(screen)
    # create timer
    clock = pygame.time.Clock()
    # create game object
    game = Game(screen, chessboard)

    # main loop
    while True:
        # event detect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # exit program

            # if nobody win，continue. otherwise show win image
            if not game.show_win:
                # detect the chess is clicked
                clicked_dot = Dot.click()
                if clicked_dot:
                    chessboard.move_chess(clicked_dot.row, clicked_dot.col)
                    # clean the chess position can be move
                    Dot.clean_last_position()
                    ClickBox.clean()
                    # detect win system
                    if chessboard.judge_attack_general(game.get_player()):
                        print("General.... ")
                        # detect another player can win the game or not
                        if chessboard.judge_win(game.get_player()):
                            print("win...")
                            game.set_win(game.get_player())
                        else:
                            # if can attack another general, show image
                            game.set_attack()
                    # exchange player after chess is placed
                    game.exchange()
                    # exit for loop
                    break

                # detect the chess
                # clicked_chess = Chess.get_clicked_chess(chessboard)
                clicked_chess = Chess.get_clicked_chess(game.get_player(), chessboard)
                if clicked_chess:
                    # create chess object which is clicked
                    ClickBox(screen, clicked_chess.row, clicked_chess.col)
                    # clean all the chess object before
                    Dot.clean_last_position()
                    # calculate the position which can be placed
                    put_down_chess_pos = chessboard.get_put_down_postion(clicked_chess)
                    Dot.create_nums_dot(screen, put_down_chess_pos)

        # show background image
        screen.blit(background_img, (0, 0))
        screen.blit(background_img, (0, 270))
        screen.blit(background_img, (0, 540))

        # # show chessboard
        # # screen.blit(chessboard_img, (50, 50))
        # chessboard.show()
        #
        # # show chess in the chessboard
        # # for line_chess in chessboard_map:
        # for line_chess in chessboard.chessboard_map:
        #     for chess in line_chess:
        #         if chess:
        #             # screen.blit(chess[0], chess[1])
        #             chess.show()

        # show chessboard and chess
        chessboard.show_chessboard_and_chess()

        # point the chess is click
        ClickBox.show()

        # show where can place the chess
        Dot.show_all()

        # show the information of the game
        game.show()

        # show the content in the screen object
        pygame.display.update()

        # FPS
        clock.tick(60)  # set FPS


if __name__ == '__main__':
    main()
