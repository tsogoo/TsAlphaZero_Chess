#!/usr/bin/env python

import numpy as np
import itertools
import copy
import chess
class board():
    def __init__(self):
        self.init_board = np.zeros([8,8]).astype(str)
        self.init_board[0,0] = "r"
        self.init_board[0,1] = "r"
        # self.init_board[0,2] = "b"
        # self.init_board[0,3] = "q"
        self.init_board[0,4] = "k"
        # self.init_board[0,5] = "b"
        # self.init_board[0,6] = "n"
        # self.init_board[0,7] = "r"
        # self.init_board[1,0:8] = "p"
        # self.init_board[7,0] = "R"
        # self.init_board[7,1] = "N"
        # self.init_board[7,2] = "B"
        # self.init_board[7,3] = "Q"
        self.init_board[7,3] = "K"
        # self.init_board[7,5] = "B"
        self.init_board[7,6] = "R"
        self.init_board[7,7] = "R"
        # self.init_board[6,0:8] = "P"
        self.init_board[self.init_board == "0.0"] = " "
        self.move_count = 0
        self.no_progress_count = 0
        self.repetitions_w = 0
        self.repetitions_b = 0
        self.move_history = None
        self.en_passant = -999; self.en_passant_move = 0 # returns j index of last en_passant pawn
        self.r1_move_count = 0 # black's queenside rook
        self.r2_move_count = 0 # black's kingside rook
        self.k_move_count = 0
        self.R1_move_count = 0 # white's queenside rook
        self.R2_move_count = 0 # white's kingside rook
        self.K_move_count = 0
        self.current_board = self.init_board
        self.en_passant_move_copy = None
        self.copy_board = None; self.en_passant_copy = None; self.r1_move_count_copy = None; self.r2_move_count_copy = None; 
        self.k_move_count_copy = None; self.R1_move_count_copy = None; self.R2_move_count_copy = None; self.K_move_count_copy = None
        self.player = 0 # current player's turn (0:white, 1:black)
        
    def move_rules_P(self,current_position):
        i, j = current_position
        next_positions = []
        board_state = self.current_board
        ## to calculate allowed moves for king
        threats = []
        if 0<=i-1<=7 and 0<=j+1<=7:
            threats.append((i-1,j+1))
        if 0<=i-1<=7 and 0<=j-1<=7:
            threats.append((i-1,j-1))
        #at initial position
        if i==6:
            if board_state[i-1,j]==" ":
                next_positions.append((i-1,j))
                if board_state[i-2,j]==" ":
                    next_positions.append((i-2,j))
        # en passant capture
        elif i==3 and self.en_passant!=-999:
            if j-1==self.en_passant and abs(self.en_passant_move-self.move_count) == 1:
                next_positions.append((i-1,j-1))
            elif j+1==self.en_passant and abs(self.en_passant_move-self.move_count) == 1:
                next_positions.append((i-1,j+1))
        if i in [1,2,3,4,5] and board_state[i-1,j]==" ":
            next_positions.append((i-1,j))          
        if j==0 and board_state[i-1,j+1] in ["r", "n", "b", "q", "k", "p"]:
            next_positions.append((i-1,j+1))
        elif j==7 and board_state[i-1,j-1] in ["r", "n", "b", "q", "k", "p"]:
            next_positions.append((i-1,j-1))
        elif j in [1,2,3,4,5,6]:
            if board_state[i-1,j+1] in ["r", "n", "b", "q", "k", "p"]:
                next_positions.append((i-1,j+1))
            if board_state[i-1,j-1] in ["r", "n", "b", "q", "k", "p"]:
                next_positions.append((i-1,j-1))
        return next_positions, threats
    
    def move_rules_p(self,current_position):
        i, j = current_position
        next_positions = []
        board_state = self.current_board
        ## to calculate allowed moves for king
        threats = []
        if 0<=i+1<=7 and 0<=j+1<=7:
            threats.append((i+1,j+1))
        if 0<=i+1<=7 and 0<=j-1<=7:
            threats.append((i+1,j-1))
        #at initial position
        if i==1:
            if board_state[i+1,j]==" ":
                next_positions.append((i+1,j))
                if board_state[i+2,j]==" ":
                    next_positions.append((i+2,j))
        # en passant capture
        elif i==4 and self.en_passant!=-999:
            if j-1==self.en_passant and abs(self.en_passant_move-self.move_count) == 1:
                next_positions.append((i+1,j-1))
            elif j+1==self.en_passant and abs(self.en_passant_move-self.move_count) == 1:
                next_positions.append((i+1,j+1))
        if i in [2,3,4,5,6] and board_state[i+1,j]==" ":
            next_positions.append((i+1,j))          
        if j==0 and board_state[i+1,j+1] in ["R", "N", "B", "Q", "K", "P"]:
            next_positions.append((i+1,j+1))
        elif j==7 and board_state[i+1,j-1] in ["R", "N", "B", "Q", "K", "P"]:
            next_positions.append((i+1,j-1))
        elif j in [1,2,3,4,5,6]:
            if board_state[i+1,j+1] in ["R", "N", "B", "Q", "K", "P"]:
                next_positions.append((i+1,j+1))
            if board_state[i+1,j-1] in ["R", "N", "B", "Q", "K", "P"]:
                next_positions.append((i+1,j-1))
        return next_positions, threats
    
    def move_rules_r(self,current_position):
        i, j = current_position
        board_state = self.current_board
        next_positions = []; a=i
        while a!=0:
            if board_state[a-1,j]!=" ":
                if board_state[a-1,j] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a-1,j))
                break
            next_positions.append((a-1,j))
            a-=1
        a=i
        while a!=7:
            if board_state[a+1,j]!=" ":
                if board_state[a+1,j] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a+1,j))
                break
            next_positions.append((a+1,j))
            a+=1
        a=j
        while a!=7:
            if board_state[i,a+1]!=" ":
                if board_state[i,a+1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((i,a+1))
                break
            next_positions.append((i,a+1))
            a+=1
        a=j
        while a!=0:
            if board_state[i,a-1]!=" ":
                if board_state[i,a-1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((i,a-1))
                break
            next_positions.append((i,a-1))
            a-=1
        return next_positions
    
    def move_rules_R(self,current_position):
        i, j = current_position
        board_state = self.current_board
        next_positions = []; a=i
        while a!=0:
            if board_state[a-1,j]!=" ":
                if board_state[a-1,j] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a-1,j))
                break
            next_positions.append((a-1,j))
            a-=1
        a=i
        while a!=7:
            if board_state[a+1,j]!=" ":
                if board_state[a+1,j] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a+1,j))
                break
            next_positions.append((a+1,j))
            a+=1
        a=j
        while a!=7:
            if board_state[i,a+1]!=" ":
                if board_state[i,a+1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((i,a+1))
                break
            next_positions.append((i,a+1))
            a+=1
        a=j
        while a!=0:
            if board_state[i,a-1]!=" ":
                if board_state[i,a-1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((i,a-1))
                break
            next_positions.append((i,a-1))
            a-=1
        return next_positions
    
    def move_rules_n(self,current_position):
        i, j = current_position
        next_positions = []
        board_state = self.current_board
        for a,b in [(i+2,j-1),(i+2,j+1),(i+1,j-2),(i-1,j-2),(i-2,j+1),(i-2,j-1),(i-1,j+2),(i+1,j+2)]:
            if 0<=a<=7 and 0<=b<=7:
                if board_state[a,b] in ["R", "N", "B", "Q", "K", "P", " "]:
                    next_positions.append((a,b))
        return next_positions
    
    def move_rules_N(self,current_position):
        i, j = current_position
        next_positions = []
        board_state = self.current_board
        for a,b in [(i+2,j-1),(i+2,j+1),(i+1,j-2),(i-1,j-2),(i-2,j+1),(i-2,j-1),(i-1,j+2),(i+1,j+2)]:
            if 0<=a<=7 and 0<=b<=7:
                if board_state[a,b] in ["r", "n", "b", "q", "k", "p", " "]:
                    next_positions.append((a,b))
        return next_positions
    
    def move_rules_b(self,current_position):
        i, j = current_position
        next_positions = []
        board_state = self.current_board
        a=i;b=j
        while a!=0 and b!=0:
            if board_state[a-1,b-1]!=" ":
                if board_state[a-1,b-1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a-1,b-1))
                break
            next_positions.append((a-1,b-1))
            a-=1;b-=1
        a=i;b=j
        while a!=7 and b!=7:
            if board_state[a+1,b+1]!=" ":
                if board_state[a+1,b+1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a+1,b+1))
                break
            next_positions.append((a+1,b+1))
            a+=1;b+=1
        a=i;b=j
        while a!=0 and b!=7:
            if board_state[a-1,b+1]!=" ":
                if board_state[a-1,b+1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a-1,b+1))
                break
            next_positions.append((a-1,b+1))
            a-=1;b+=1
        a=i;b=j
        while a!=7 and b!=0:
            if board_state[a+1,b-1]!=" ":
                if board_state[a+1,b-1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a+1,b-1))
                break
            next_positions.append((a+1,b-1))
            a+=1;b-=1
        return next_positions
    
    def move_rules_B(self,current_position):
        i, j = current_position
        next_positions = []
        board_state = self.current_board
        a=i;b=j
        while a!=0 and b!=0:
            if board_state[a-1,b-1]!=" ":
                if board_state[a-1,b-1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a-1,b-1))
                break
            next_positions.append((a-1,b-1))
            a-=1;b-=1
        a=i;b=j
        while a!=7 and b!=7:
            if board_state[a+1,b+1]!=" ":
                if board_state[a+1,b+1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a+1,b+1))
                break
            next_positions.append((a+1,b+1))
            a+=1;b+=1
        a=i;b=j
        while a!=0 and b!=7:
            if board_state[a-1,b+1]!=" ":
                if board_state[a-1,b+1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a-1,b+1))
                break
            next_positions.append((a-1,b+1))
            a-=1;b+=1
        a=i;b=j
        while a!=7 and b!=0:
            if board_state[a+1,b-1]!=" ":
                if board_state[a+1,b-1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a+1,b-1))
                break
            next_positions.append((a+1,b-1))
            a+=1;b-=1
        return next_positions
    
    def move_rules_q(self,current_position):
        i, j = current_position
        board_state = self.current_board
        next_positions = [];a=i
        #bishop moves
        while a!=0:
            if board_state[a-1,j]!=" ":
                if board_state[a-1,j] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a-1,j))
                break
            next_positions.append((a-1,j))
            a-=1
        a=i
        while a!=7:
            if board_state[a+1,j]!=" ":
                if board_state[a+1,j] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a+1,j))
                break
            next_positions.append((a+1,j))
            a+=1
        a=j
        while a!=7:
            if board_state[i,a+1]!=" ":
                if board_state[i,a+1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((i,a+1))
                break
            next_positions.append((i,a+1))
            a+=1
        a=j
        while a!=0:
            if board_state[i,a-1]!=" ":
                if board_state[i,a-1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((i,a-1))
                break
            next_positions.append((i,a-1))
            a-=1
        #rook moves
        a=i;b=j
        while a!=0 and b!=0:
            if board_state[a-1,b-1]!=" ":
                if board_state[a-1,b-1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a-1,b-1))
                break
            next_positions.append((a-1,b-1))
            a-=1;b-=1
        a=i;b=j
        while a!=7 and b!=7:
            if board_state[a+1,b+1]!=" ":
                if board_state[a+1,b+1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a+1,b+1))
                break
            next_positions.append((a+1,b+1))
            a+=1;b+=1
        a=i;b=j
        while a!=0 and b!=7:
            if board_state[a-1,b+1]!=" ":
                if board_state[a-1,b+1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a-1,b+1))
                break
            next_positions.append((a-1,b+1))
            a-=1;b+=1
        a=i;b=j
        while a!=7 and b!=0:
            if board_state[a+1,b-1]!=" ":
                if board_state[a+1,b-1] in ["R", "N", "B", "Q", "K", "P"]:
                    next_positions.append((a+1,b-1))
                break
            next_positions.append((a+1,b-1))
            a+=1;b-=1
        return next_positions
    
    def move_rules_Q(self,current_position):
        i, j = current_position
        board_state = self.current_board
        next_positions = [];a=i
        #bishop moves
        while a!=0:
            if board_state[a-1,j]!=" ":
                if board_state[a-1,j] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a-1,j))
                break
            next_positions.append((a-1,j))
            a-=1
        a=i
        while a!=7:
            if board_state[a+1,j]!=" ":
                if board_state[a+1,j] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a+1,j))
                break
            next_positions.append((a+1,j))
            a+=1
        a=j
        while a!=7:
            if board_state[i,a+1]!=" ":
                if board_state[i,a+1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((i,a+1))
                break
            next_positions.append((i,a+1))
            a+=1
        a=j
        while a!=0:
            if board_state[i,a-1]!=" ":
                if board_state[i,a-1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((i,a-1))
                break
            next_positions.append((i,a-1))
            a-=1
        #rook moves
        a=i;b=j
        while a!=0 and b!=0:
            if board_state[a-1,b-1]!=" ":
                if board_state[a-1,b-1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a-1,b-1))
                break
            next_positions.append((a-1,b-1))
            a-=1;b-=1
        a=i;b=j
        while a!=7 and b!=7:
            if board_state[a+1,b+1]!=" ":
                if board_state[a+1,b+1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a+1,b+1))
                break
            next_positions.append((a+1,b+1))
            a+=1;b+=1
        a=i;b=j
        while a!=0 and b!=7:
            if board_state[a-1,b+1]!=" ":
                if board_state[a-1,b+1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a-1,b+1))
                break
            next_positions.append((a-1,b+1))
            a-=1;b+=1
        a=i;b=j
        while a!=7 and b!=0:
            if board_state[a+1,b-1]!=" ":
                if board_state[a+1,b-1] in ["r", "n", "b", "q", "k", "p"]:
                    next_positions.append((a+1,b-1))
                break
            next_positions.append((a+1,b-1))
            a+=1;b-=1
        return next_positions
    
    #does not include king, castling
    def possible_W_moves(self, threats=False):
        board_state = self.current_board
        rooks = {}; knights = {}; bishops = {}; queens = {}; pawns = {};

        opponent_king_pos = np.where(board_state == "k")
        if opponent_king_pos[0].size > 0:  # Ensure the black king is on the board
            opponent_king_pos = (opponent_king_pos[0][0], opponent_king_pos[1][0])
        else:
            opponent_king_pos = None  # Safety check in case the black king is not found
        i, j = np.where(board_state == "R")
        for rook in zip(i, j):
            rooks[tuple(rook)] = [move for move in self.move_rules_R(rook) if move != opponent_king_pos]
        
        # Generate knight moves and filter out moves to the black king's position
        i, j = np.where(board_state == "N")
        for knight in zip(i, j):
            knights[tuple(knight)] = [move for move in self.move_rules_N(knight) if move != opponent_king_pos]
        
        # Generate bishop moves and filter out moves to the black king's position
        i, j = np.where(board_state == "B")
        for bishop in zip(i, j):
            bishops[tuple(bishop)] = [move for move in self.move_rules_B(bishop) if move != opponent_king_pos]
        
        # Generate queen moves and filter out moves to the black king's position
        i, j = np.where(board_state == "Q")
        for queen in zip(i, j):
            queens[tuple(queen)] = [move for move in self.move_rules_Q(queen) if move != opponent_king_pos]
    
        for queen in zip(i,j):
            queens[tuple(queen)] = self.move_rules_Q(queen)
        i,j = np.where(board_state=="P")
        for pawn in zip(i,j):
            if threats==False:
                pawns[tuple(pawn)],_ = self.move_rules_P(pawn)
                pawns[tuple(pawn)] = [move for move in pawn_moves if move != opponent_king_pos]
            else:
                _,pawns[tuple(pawn)] = self.move_rules_P(pawn)
                pawns[tuple(pawn)] = [move for move in pawn_threats if move != opponent_king_pos]
        c_dict = {"R": rooks, "N": knights, "B": bishops, "Q": queens, "P": pawns}
        c_list = []
        c_list.extend(list(itertools.chain(*list(rooks.values())))); c_list.extend(list(itertools.chain(*list(knights.values())))); 
        c_list.extend(list(itertools.chain(*list(bishops.values())))); c_list.extend(list(itertools.chain(*list(queens.values()))))
        c_list.extend(list(itertools.chain(*list(pawns.values()))))
        return c_list, c_dict
        
    def move_rules_k(self):
        current_position = np.where(self.current_board=="k")
        i, j = current_position; i,j = i[0],j[0]
        next_positions = []
        c_list, _ = self.possible_W_moves(threats=True)
        for a,b in [(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i+1,j+1),(i-1,j-1),(i+1,j-1),(i-1,j+1)]:
            if 0<=a<=7 and 0<=b<=7:
                if self.current_board[a,b] in [" ","Q","B","N","P","R"] and (a,b) not in c_list:
                    next_positions.append((a,b))
        if self.castle("queenside") == True and self.check_status() == False:
            next_positions.append((0,2))
        if self.castle("kingside") == True and self.check_status() == False:
            next_positions.append((0,6))
        return next_positions
    
        #does not include king, castling
    def possible_B_moves(self,threats=False):
        rooks = {}; knights = {}; bishops = {}; queens = {}; pawns = {};
        board_state = self.current_board
        opponent_king_pos = np.where(board_state == "K")
        if opponent_king_pos[0].size > 0:  # Ensure the black king is on the board
            opponent_king_pos = (opponent_king_pos[0][0], opponent_king_pos[1][0])
        else:
            opponent_king_pos = None  # Safety check in case the black king is not found
        i, j = np.where(board_state == "r")
        for rook in zip(i, j):
            rooks[tuple(rook)] = [move for move in self.move_rules_R(rook) if move != opponent_king_pos]
        
        # Generate knight moves and filter out moves to the black king's position
        i, j = np.where(board_state == "n")
        for knight in zip(i, j):
            knights[tuple(knight)] = [move for move in self.move_rules_N(knight) if move != opponent_king_pos]
        
        # Generate bishop moves and filter out moves to the black king's position
        i, j = np.where(board_state == "b")
        for bishop in zip(i, j):
            bishops[tuple(bishop)] = [move for move in self.move_rules_B(bishop) if move != opponent_king_pos]
        
        # Generate queen moves and filter out moves to the black king's position
        i, j = np.where(board_state == "q")
        for queen in zip(i, j):
            queens[tuple(queen)] = [move for move in self.move_rules_Q(queen) if move != opponent_king_pos]
    
        for queen in zip(i,j):
            queens[tuple(queen)] = self.move_rules_Q(queen)
        i,j = np.where(board_state=="p")
        for pawn in zip(i,j):
            if threats==False:
                pawns[tuple(pawn)],_ = self.move_rules_P(pawn)
                pawns[tuple(pawn)] = [move for move in pawn_moves if move != opponent_king_pos]
            else:
                _,pawns[tuple(pawn)] = self.move_rules_P(pawn)
                pawns[tuple(pawn)] = [move for move in pawn_threats if move != opponent_king_pos]
        c_dict = {"r": rooks, "n": knights, "b": bishops, "q": queens, "p": pawns}
        c_list = []
        c_list.extend(list(itertools.chain(*list(rooks.values())))); c_list.extend(list(itertools.chain(*list(knights.values())))); 
        c_list.extend(list(itertools.chain(*list(bishops.values())))); c_list.extend(list(itertools.chain(*list(queens.values()))))
        c_list.extend(list(itertools.chain(*list(pawns.values()))))
        return c_list, c_dict
        
    def move_rules_K(self):
        current_position = np.where(self.current_board=="K")
        i, j = current_position; i,j = i[0],j[0]
        next_positions = []
        c_list, _ = self.possible_B_moves(threats=True)
        for a,b in [(i+1,j),(i-1,j),(i,j+1),(i,j-1),(i+1,j+1),(i-1,j-1),(i+1,j-1),(i-1,j+1)]:
            if 0<=a<=7 and 0<=b<=7:
                if self.current_board[a,b] in [" ","q","b","n","p","r"] and (a,b) not in c_list:
                    next_positions.append((a,b))
        if self.castle("queenside") == True and self.check_status() == False:
            next_positions.append((7,2))
        if self.castle("kingside") == True and self.check_status() == False:
            next_positions.append((7,6))
        return next_positions
    
    def move_piece(self,initial_position,final_position,promoted_piece="Q"):
        if self.player == 0:
            promoted = False
            i, j = initial_position
            piece = self.current_board[i,j]
            self.current_board[i,j] = " "
            i, j = final_position
            if piece == "R" and initial_position == (7,0):
                self.R1_move_count += 1
            if piece == "R" and initial_position == (7,7):
                self.R2_move_count += 1
            if piece == "K":
                self.K_move_count += 1
            x, y = initial_position
            if piece == "P":
                if abs(x-i) > 1:
                    self.en_passant = j; self.en_passant_move = self.move_count
                if abs(y-j) == 1 and self.current_board[i,j] == " ": # En passant capture
                    self.current_board[i+1,j] = " "
                if i == 0 and promoted_piece in ["R","B","N","Q"]:
                    self.current_board[i,j] = promoted_piece
                    promoted = True
            if promoted == False:
                self.current_board[i,j] = piece
            self.player = 1
            self.move_count += 1
    
        elif self.player == 1:
            promoted = False
            i, j = initial_position
            piece = self.current_board[i,j]
            self.current_board[i,j] = " "
            i, j = final_position
            if piece == "r" and initial_position == (0,0):
                self.r1_move_count += 1
            if piece == "r" and initial_position == (0,7):
                self.r2_move_count += 1
            if piece == "k":
                self.k_move_count += 1
            x, y = initial_position
            if piece == "p":
                if abs(x-i) > 1:
                    self.en_passant = j; self.en_passant_move = self.move_count
                if abs(y-j) == 1 and self.current_board[i,j] == " ": # En passant capture
                    self.current_board[i-1,j] = " "
                if i == 7 and promoted_piece in ["r","b","n","q"]:
                    self.current_board[i,j] = promoted_piece
                    promoted = True
            if promoted == False:
                self.current_board[i,j] = piece
            self.player = 0
            self.move_count += 1

        else:
            print("Invalid move: ",initial_position,final_position,promoted_piece)
        
        
    ## player = "w" or "b", side="queenside" or "kingside"
    def castle(self,side,inplace=False):
        if self.player == 0 and self.K_move_count == 0:
            if side == "queenside" and self.R1_move_count == 0 and self.current_board[7,1] == " " and self.current_board[7,2] == " "\
                and self.current_board[7,3] == " ":
                if inplace == True:
                    self.current_board[7,0] = " "; self.current_board[7,3] = "R"
                    self.current_board[7,4] = " "; self.current_board[7,2] = "K"
                    self.K_move_count += 1
                    self.player = 1
                return True
            elif side == "kingside" and self.R2_move_count == 0 and self.current_board[7,5] == " " and self.current_board[7,6] == " ":
                if inplace == True:
                    self.current_board[7,7] = " "; self.current_board[7,5] = "R"
                    self.current_board[7,4] = " "; self.current_board[7,6] = "K"
                    self.K_move_count += 1
                    self.player = 1
                return True
        if self.player == 1 and self.k_move_count == 0:
            if side == "queenside" and self.r1_move_count == 0 and self.current_board[0,1] == " " and self.current_board[0,2] == " "\
                and self.current_board[0,3] == " ":
                if inplace == True:
                    self.current_board[0,0] = " "; self.current_board[0,3] = "r"
                    self.current_board[0,4] = " "; self.current_board[0,2] = "k"
                    self.k_move_count += 1
                    self.player = 0
                return True
            elif side == "kingside" and self.r2_move_count == 0 and self.current_board[0,5] == " " and self.current_board[0,6] == " ":
                if inplace == True:
                    self.current_board[0,7] = " "; self.current_board[0,5] = "r"
                    self.current_board[0,4] = " "; self.current_board[0,6] = "k"
                    self.k_move_count += 1
                    self.player = 0
                return True
        return False
    
    ## Check if current player's king is in check
    def check_status(self):
        board = self.convert_current_board_to_chess_board()
        if board.is_check():
            return True
        return False
       
    
    def in_check_possible_moves(self):
        return self.actions()
        self.copy_board = copy.deepcopy(self.current_board); self.move_count_copy = self.move_count # backup board state
        self.en_passant_copy = copy.deepcopy(self.en_passant); self.r1_move_count_copy = copy.deepcopy(self.r1_move_count); 
        self.r2_move_count_copy = copy.deepcopy(self.r2_move_count); self.en_passant_move_copy = copy.deepcopy(self.en_passant_move)
        self.k_move_count_copy = copy.deepcopy(self.k_move_count); self.R1_move_count_copy = copy.deepcopy(self.R1_move_count); 
        self.R2_move_count_copy = copy.deepcopy(self.R2_move_count)
        self.K_move_count_copy = copy.deepcopy(self.K_move_count)
        if self.player == 0:
            possible_moves = []
            _, c_dict = self.possible_W_moves()
            current_position = np.where(self.current_board=="K")
            i, j = current_position; i,j = i[0],j[0]
            c_dict["K"] = {(i,j):self.move_rules_K()}
            for key in c_dict.keys():
                for initial_pos in c_dict[key].keys():
                    for final_pos in c_dict[key][initial_pos]:
                        self.move_piece(initial_pos,final_pos)
                        self.player = 0 # reset board
                        if self.check_status() == False:
                            possible_moves.append([initial_pos, final_pos])
                        self.current_board = copy.deepcopy(self.copy_board);
                        self.en_passant = copy.deepcopy(self.en_passant_copy); self.en_passant_move = copy.deepcopy(self.en_passant_move_copy)
                        self.R1_move_count = copy.deepcopy(self.R1_move_count_copy); self.R2_move_count = copy.deepcopy(self.R2_move_count_copy)
                        self.K_move_count = copy.deepcopy(self.K_move_count_copy); self.move_count = self.move_count_copy
            return possible_moves
        if self.player == 1:
            possible_moves = []
            _, c_dict = self.possible_B_moves()
            current_position = np.where(self.current_board=="k")
            i, j = current_position; i,j = i[0],j[0]
            c_dict["k"] = {(i,j):self.move_rules_k()}
            for key in c_dict.keys():
                for initial_pos in c_dict[key].keys():
                    for final_pos in c_dict[key][initial_pos]:
                        self.move_piece(initial_pos,final_pos)
                        self.player = 1 # reset board
                        if self.check_status() == False:
                            possible_moves.append([initial_pos, final_pos])
                        self.current_board = copy.deepcopy(self.copy_board);
                        self.en_passant = copy.deepcopy(self.en_passant_copy); self.en_passant_move = copy.deepcopy(self.en_passant_move_copy)
                        self.r1_move_count = copy.deepcopy(self.r1_move_count_copy); self.r2_move_count = copy.deepcopy(self.r2_move_count_copy)
                        self.k_move_count = copy.deepcopy(self.k_move_count_copy); self.move_count = self.move_count_copy
            return possible_moves
    
    # convert current board to python-chess board
    def convert_current_board_to_chess_board(self):
        board = chess.Board()
        if self.player:
            board.turn = chess.BLACK
        else:
            board.turn = chess.WHITE
        # if self.en_passant != None:
        #     board.ep_square = chess.square(self.en_passant,0) if self.player == 0 else chess.square(self.en_passant,5)
        castling_fen = ""
        if self.K_move_count == 0:
            if self.R1_move_count == 0:
                if self.R2_move_count == 0:
                    castling_fen += "QK"
                else:
                    castling_fen += "Q"
            else:
                if self.R2_move_count == 0:
                    castling_fen += "K"
        if self.k_move_count == 0:
            if self.r1_move_count == 0:
                if self.r2_move_count == 0:
                    castling_fen += "qk"
                else:
                    castling_fen += "q"
            else:
                if self.r2_move_count == 0:
                    castling_fen += "k"
        if castling_fen == "":
            castling_fen = "-"
        # board.set_castling_fen(castling_fen)
            
        for i in range(8):
            for j in range(8):
                if self.current_board[i,j] == "P":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.PAWN,chess.WHITE))
                elif self.current_board[i,j] == "R":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.ROOK,chess.WHITE))
                elif self.current_board[i,j] == "N":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.KNIGHT,chess.WHITE))
                elif self.current_board[i,j] == "B":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.BISHOP,chess.WHITE))
                elif self.current_board[i,j] == "Q":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.QUEEN,chess.WHITE))
                elif self.current_board[i,j] == "K":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.KING,chess.WHITE))
                elif self.current_board[i,j] == "p":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.PAWN,chess.BLACK))
                elif self.current_board[i,j] == "r":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.ROOK,chess.BLACK))
                elif self.current_board[i,j] == "n":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.KNIGHT,chess.BLACK))
                elif self.current_board[i,j] == "b":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.BISHOP,chess.BLACK))
                elif self.current_board[i,j] == "q":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.QUEEN,chess.BLACK))
                elif self.current_board[i,j] == "k":
                    board.set_piece_at(chess.square(j,7-i),chess.Piece(chess.KING,chess.BLACK))
                else:
                    board.set_piece_at(chess.square(j,7-i),None)
        return board

    def is_adjacent(self, pos1, pos2):
        row_diff = abs(pos1[0] - pos2[0])
        col_diff = abs(pos1[1] - pos2[1])
        return row_diff <= 1 and col_diff <= 1

    def convert_chess_move_to_action(self, move):
        promotion = None
        if move.promotion:
            if move.promotion == 5:
                promotion = "queen"
            elif move.promotion == 4:
                promotion = "rook"
            elif move.promotion == 3:
                promotion = "bishop"
            elif move.promotion == 2:
                promotion = "knight"        
        return (7 - move.from_square // 8, move.from_square % 8), (7 - move.to_square // 8, move.to_square % 8), promotion

    def actions(self): # returns all possible actions while not in check: initial_pos,final_pos,underpromote
        board = self.convert_current_board_to_chess_board()
        acts = []
        for move in board.legal_moves:
            acts.append(self.convert_chess_move_to_action(move))
        return acts
