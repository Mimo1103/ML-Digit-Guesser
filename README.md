# Handwritten Digit Recognizer (CNN)
## Overview
A machine learning application that recognizes handwritten digits (0-9) using a Convolutional Neural Network (CNN)

The user can draw a digit in a graphical user interface and the model predicts the number as well as the corresponding probability score

## How it works
1. The user draws a digit in the GUI
2. The drawing is processed and converted into a format compatible with the model
3. The CNN predicts the digit
4. The probabilities for each digit (0-9) are displayed from most-likely to least-likely

## Features
- Handwritten digit recognition (0-9)
- Graphical user interface for drawing input
- Real-time prediction with probability output
- Visualization of the processed input image
- Improved accuracy through additional fine-tuning

## Model & Training
- CNN is trained on the MNIST dataset
- Further improved using a custom built fine-tuning dataset
- Fine-tuning helped better distinction between similar digits (eg. 1 and 7)
- Improved recognition of different writing styles (eg. variations of 4)

## My contribution
- Trained the CNN using TensorFlow based on documentation
- Implemented preprocessing for user input
- Created a custom fine-tuning dataset
- Built the GUI and connected it to the model

## Technologies
- Python
- TensorFlow
- NumPy
- PyQt5
- OpenCV

## Example
Here is the GUI of the Handwritten Digit Recognizer, where the user draws a number and sees the predicted probabilities:
![ML_Digit_Recognizer_GUI](https://github.com/user-attachments/assets/bc5eff98-4b58-4ac4-a212-1e48da2dce70)

