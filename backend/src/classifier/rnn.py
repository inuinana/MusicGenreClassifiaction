#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on sleepy midnight in Aug
@author: Akihiro Inui
"""

from __future__ import print_function
import os
import numpy as np
import cloudpickle
import torch
import torch.onnx
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import tqdm
from torch.autograd import Variable


class RNNModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super(RNNModel, self).__init__()
        # Number of hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.layer_dim = layer_dim

        # RNN
        self.rnn = nn.RNN(input_dim, hidden_dim, layer_dim, batch_first=True,
                          nonlinearity='relu')

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = Variable(torch.zeros(self.layer_dim, x.size(0), self.hidden_dim))

        # One time step
        out, hn = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out


class CustomRNN:
    def __init__(self, validation_rate, num_classes):
        self.validation_rate = validation_rate
        self.num_classes = num_classes

        self.model = RNNModel(input_dim=64, hidden_dim=10, layer_dim=10, output_dim=num_classes)

        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_function = nn.CrossEntropyLoss()

    def training(self, train_loader, validation_loader, visualize=True):
        # To log losses
        train_loss_history = []
        train_accuracy_history = []
        validation_loss_history = []
        validation_accuracy_history = []
        for epoch in range(1, 200):
            # Set to train mode
            # self.model.train()

            # Iteration for batch
            batch_accuracy = 0
            batch_loss = 0
            sample_num = 0
            for batch_idx, (data, label) in tqdm.tqdm(enumerate(train_loader)):
                # Define hardware
                data = data.to("cpu")
                label = label.to("cpu")

                # Forward data and calculate loss
                # data = data.unsqueeze(1)  # Make 3D array to 4D
                output = self.model(data)

                _, prediction = output.max(1)
                loss = self.loss_function(output, label)

                # Delete gradient value calculated in previous epoch
                self.optimizer.zero_grad()

                # Log loss
                batch_loss += loss.item()
                loss.backward()

                # Update optimizer
                self.optimizer.step()

                # Calculate batch accuracy
                batch_accuracy += (label == prediction).float().sum().item()

                # Update counter
                sample_num += len(data)

            # Append train accuracy and loss
            train_accuracy_history.append(100*batch_accuracy/sample_num)
            train_loss_history.append(batch_loss/sample_num)

            # Print training status
            print(train_loss_history[-1], train_accuracy_history[-1], flush=True)

            # Validation
            validation_loss, validation_accuracy = self.validation(self.model, validation_loader)
            validation_accuracy_history.append(validation_accuracy)
            validation_loss_history.append(validation_loss)
            # Print validation status
            print(validation_loss_history[-1], validation_accuracy_history[-1], flush=True)

        if visualize is True:
            plt.plot(train_accuracy_history)
            plt.plot(validation_accuracy_history)
            plt.title('model accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train', 'validation'], loc='upper left')
            plt.show()

            # Loss
            plt.plot(train_loss_history)
            plt.plot(validation_loss_history)
            plt.title('model loss')
            plt.ylabel('loss')
            plt.xlabel('epoch')
            plt.legend(['train', 'validation'], loc='upper left')
            plt.show()

        return self.model

    def validation(self, model, validation_loader):
        # Set to evaluation mode
        model.eval()

        # Iteration for batch
        batch_accuracy = 0
        batch_loss = 0
        sample_num = 0
        for batch_idx, (data, label) in enumerate(validation_loader):
            # Define hardware
            data = data.to("cpu")
            label = label.to("cpu")

            # Forward data and calculate loss
            # data = data.unsqueeze(1)  # Make 3D array to 4D
            with torch.no_grad():
                output = model(data)
                _, prediction = output.max(1)
            loss = self.loss_function(output, label)

            # Log loss
            batch_loss += loss.item()

            # Calculate batch accuracy
            batch_accuracy += (label == prediction).float().sum().item()

            # Update counter
            sample_num += len(data)

        # Append accuracy and loss
        validation_accuracy = 100*batch_accuracy/sample_num
        validation_loss = batch_loss/sample_num
        return validation_loss, validation_accuracy

    def test(self, model, test_loader):

        # Set to evaluation mode
        model.eval()

        # Iteration for batch
        batch_accuracy = 0
        sample_num = 0
        for batch_idx, (data, label) in enumerate(test_loader):
            # Define hardware
            data = data.to("cpu")
            label = label.to("cpu")

            # Forward data and calculate loss
            # data = data.unsqueeze(1)  # Make 3D array to 4D
            with torch.no_grad():
                output = model(data)
                _, prediction = output.max(1)

            # Calculate batch accuracy
            batch_accuracy += (label == prediction).float().sum().item()

            # Update counter
            sample_num += len(data)

        test_accuracy = 100*batch_accuracy/sample_num
        return test_accuracy

    def predict(self, model, target_data):
        """
        Make prediction to a given target data and return the prediction result with accuracy for each sample
        :param  model: trained model
        :param  target_data: target data without label
        :return prediction array with probability
        """
        # Make prediction to the target data
        return model(torch.tensor(np.array(target_data), dtype=torch.float32))

    def load_model(self, model_file_name: str):
        """
        Load trained model
        :param  model_file_name: name of model file to load
        :return model: trained model
        """
        # Load model if it exists
        assert os.path.exists(model_file_name), "Given model file does not exist"
        return torch.load(model_file_name, map_location="cpu")

    def save_model(self, model, output_directory: str):
        """
        Save model
        :param  model: trained model
        :param  output_directory: output directory path
        """
        with open(os.path.join(output_directory, "rnn.pkl"), 'wb') as f:
            cloudpickle.dump(model, f)

