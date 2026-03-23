# Handwritten Digit Recognizer (CNN)
## Overview
A machine learning application that recognizes handwritten digits (0-9) using a Convolutional Neural Network (CNN).
The user can draw a digit in a graphical user interface (GUI) and the model predicts the digit along with its probability score.

## How it works
1. The user draws a digit in the GUI
2. The drawing is processed and converted into a format compatible with the model
3. The CNN predicts the digit
4. The probabilities for each digit (0 - 9) are displayed in descending order of probability.

## Features
- Handwritten digit recognition (0 - 9)
- Graphical user interface for drawing digits
- Real-time prediction with probability output
- Visualization of the processed input image
- Improved accuracy through additional fine-tuning

## Model & Training
- CNN is trained on the MNIST dataset
- Further improved using a custom built fine-tuning dataset
- Fine-tuning improved distinction between similar digits (e.g. 1 and 7)
- Improved recognition of different writing styles (e.g. variations of 4)

## My contribution
- Designed and trained the CNN using TensorFlow, following best practices from documentation
- Implemented preprocessing for user input
- Created a custom fine-tuning dataset
- Developed the GUI and integrated it with the trained model

## Technologies
- Python
- TensorFlow
- NumPy
- PyQt5
- OpenCV

## Example
### GUI Screenshot
<img width="1121" height="721" alt="Digit Recognizer GUI Screenshot" src="https://github.com/user-attachments/assets/f870a42e-cdd1-45ab-886b-3f2ed2e981d6"/>
*The user draws a digit on the canvas and the CNN predicts the number with the corresponding probability scores.*

### Demo GIF
The GIF demonstrates the CNN predicting digits in real-time as the user draws them:
![Digit_Recognizer_Usage_GIF](https://github.com/user-attachments/assets/69b62531-e0f4-4d55-bd87-a77d09aa1340)
*Shows real-time prediction and probability output.*
