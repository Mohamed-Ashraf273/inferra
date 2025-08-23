# Sound Classification with Au57

## Overview

This project implements a **sound classification system** using a deep convolutional neural network called **Au57**, based on residual blocks. It is designed to classify environmental sounds into **50 categories** using the **ESC-50 dataset**.

The system works by converting audio clips into **spectrograms** and feeding them into the Au57 model, which extracts features through multiple convolutional and residual layers before producing class predictions.

---

## Features

- **Deep Residual CNN:** Au57 uses residual blocks to allow deep network architectures without vanishing gradient issues.  
- **Single-channel input:** Designed to work with mono audio spectrograms.  
- **Robust classification:** Capable of accurately classifying 50 different environmental sound categories.  
- **Flexible:** Can be adapted to other audio classification tasks with different datasets.  

---

## Author

**Mohamed Ashraf**

---

## Usage

The project can be used to:

- Classify environmental sounds in research or hobby projects.  
- Build real-time sound recognition systems.  
- Experiment with deep learning architectures for audio tasks.  

---

## Dataset

The project uses the **ESC-50 dataset**, which contains:

- 2,000 audio clips of 5 seconds each  
- 50 sound categories  
- Standard train/validation split for model evaluation  
