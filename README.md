# Handwritten Digit Recognizer (CNN)
## Overview
A machine learning application that recognizes handwritten digits (0-9) using a Convolutional Neural Network (CNN).

The user can draw a digit in a graphical user interface and the model predicts thr number aswell as the corresponding probability score.

## How it works
1. The user draws a digit in the GUI
2. The drawing is processed and converted into a format compatible with the model.
3. The CNN predicts the digit.
4. The probabilities for each digit (0-9) are displayed from most-likely to least-likely.

## Features
- Handwritten digit recognition (0-9).
- Graphical user interface for drawing input.
- Real-time prediction with probability output.
- Visualization of the processed input image.
- Improved accuracy through additional fine-tuning

## Model & Training
- Trained on the MNIST dataset
- Further improved using a custom made fine-tuning dataset
- Finetuning helped better distinction between 7, 1 and 4
- Recognition of different writing styles (eg. variations of 4)


## Technologies
- Python
- TensorFlow
- NumPy
- PyQt5
