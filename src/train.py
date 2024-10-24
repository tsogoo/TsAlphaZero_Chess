#!/usr/bin/env python

from alpha_net import ChessNet, train
import os
import pickle
import numpy as np
import torch


def train_chessnet(
    net_to_train="initial_model.pth.tar", save_as="trained1_iter7.pth.tar"
):
    # gather data

    for i in ["iter0", "iter1", "iter2"]:
        data_path = f"./datasets/{i}/"
        datasets = []
        for idx, file in enumerate(os.listdir(data_path)):
            filename = os.path.join(data_path, file)
            if os.path.isfile(filename):
                with open(filename, "rb") as fo:
                    datasets.extend(pickle.load(fo, encoding="bytes"))

    # train net
    net = ChessNet()
    cuda = torch.cuda.is_available()
    if cuda:
        net.cuda()
    if net_to_train:
        current_net_filename = os.path.join("./model_data/", net_to_train)
        if os.path.exists(current_net_filename):
            checkpoint = torch.load(current_net_filename)
            net.load_state_dict(checkpoint["state_dict"])
            print("Loaded model")
        train(net, datasets)
    # save results
    torch.save({"state_dict": net.state_dict()}, os.path.join("./model_data/", save_as))


if __name__ == "__main__":
    # create initial model
    # train_chessnet(net_to_train="", save_as="initial_model.pth.tar")
    train_chessnet(net_to_train="initial_model.pth", save_as="trained_model_1.pth.tar")
