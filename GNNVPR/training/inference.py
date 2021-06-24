"""Runs Inference on a specified input benchmark from a specified model.
"""
import PyTorchGeometricTrain
from optparse import OptionParser
import pandas as pd
import torch
import glob
import os
import math
import shutil
from shutil import copyfile
from torch_geometric.data import DataLoader

embed_dim = 128


# from PyTorchGeometricTrain import GraNNy_ViPeR
# from PyTorchGeometricTrain import GNNDataset

def main(options):
    proc_dir = options.inputDirectory+"processed/"
    for file in glob.glob(os.path.join(proc_dir, "*.pt")):
        os.remove(file)
    dest_dir = options.inputDirectory+"raw/"
    for file in glob.glob(os.path.join(options.inputDirectory, "*.csv")):
        shutil.copy(file, os.path.join(dest_dir, os.path.basename(file)))
    model = PyTorchGeometricTrain.GraNNy_ViPeR().to('cpu')
    model.load_state_dict(torch.load('/home/spicygremlin/Github/CS220/model.pt'))
    model.eval()

    dataset = PyTorchGeometricTrain.GNNDataset(options.inputDirectory,
                                               options.inputDirectory,
                                               options.outputDirectory)
    test_loader = DataLoader(dataset, batch_size=1)

    for data in test_loader:
        data = data.to('cpu')
        pred = model(data).detach().cpu().numpy()
        # print(pred)
        df = pd.DataFrame.from_dict(pred)
        # print("honkers")
        # df = (df-df.min())/(df.max() - df.min())
        # df = df * 8
        # def sigmoid(x):
        #     return 1 / (1.0 + math.exp(-x))
        # df = df.apply(sigmoid, axis=1)
        df = df*4
        print(df)
        print("Saving file to: ", os.getcwd())
        df.to_csv('prediction.csv', index=False,
                  header=False)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--inputDirectory", dest="inputDirectory",
                      help="directory that contains the benchmarks to be run",
                      metavar="INPUT")
    # ! Add an option to load in a saved model. 
    parser.add_option("-o", "--outputDirectory", dest="outputDirectory",
                      help="directory to output the completed model" +
                      "and metrics",
                      metavar="OUTPUT")
    # Get Arch Name
    #
    # Get Circuit Name
    #
    parser.add_option("-r", "--rootDirectory", dest="rootDirectory",
                      help="directory to output the completed model" +
                      "and metrics",
                      metavar="OUTPUT")
    (options, args) = parser.parse_args()
    # calling main function
    main(options)