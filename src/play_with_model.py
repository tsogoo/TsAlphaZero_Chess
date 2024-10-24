import numpy as np
from MCTS_chess import UCT_search, do_decode_n_move_pieces, get_policy
import encoder_decoder as ed
from chess_board import board as c_board
import copy
import torch
import os
from alpha_net import ChessNet


def play(chessnet):
    current_board = c_board()
    checkmate = False
    dataset = [] # to get state, policy, value for neural network training
    states = []
    value = 0
    player = 1
    while checkmate == False and current_board.move_count <= 100:
        draw_counter = 0
        for s in states:
            if np.array_equal(current_board.current_board,s):
                draw_counter += 1
        if draw_counter == 3: # draw by repetition
            break
        states.append(copy.deepcopy(current_board.current_board))
        board_state = copy.deepcopy(ed.encode_board(current_board))
        if player == 1:
            best_move, root = UCT_search(current_board,777,chessnet, 1, False)
            print(best_move)
            player = -1
            current_board = do_decode_n_move_pieces(current_board, best_move)
        else:
            initial_pos = input("Initial piece pos(format: 0,0): ") # 10
            final_pos = input("Final piece pos(format 7,0): ") # 12
            your_move = ed.encode_action(current_board,
                    (int(initial_pos.split(',')[0]), int(initial_pos.split(',')[1])),
                    (int(final_pos.split(',')[0]), int(final_pos.split(',')[1])))
            print("your_move", your_move)
            player = 1
            current_board = do_decode_n_move_pieces(current_board, your_move)
        
        print(current_board.current_board,current_board.move_count); print(" ")
        if current_board.check_status() == True and current_board.in_check_possible_moves() == []: # checkmate
            if current_board.player == 0: # black wins
                value = -1
            elif current_board.player == 1: # white wins
                value = 1
            checkmate = True
            print("checkmate! value: {value} is won!", value)


if __name__ == "__main__":
    net = ChessNet()
    cuda = torch.cuda.is_available()
    if cuda:
        net.cuda()
    net.share_memory()
    net.eval()

    current_net_filename = os.path.join("./model_data/trained1_iter3.pth.tar")
    checkpoint = torch.load(current_net_filename)
    net.load_state_dict(checkpoint['state_dict'])

    play(net)
