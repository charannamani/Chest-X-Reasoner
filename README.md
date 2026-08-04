# ChestX-Reasoner

An AI-powered medical imaging system for chest X-ray disease diagnosis with explainable reasoning generation.

## Overview

ChestX-Reasoner is an end-to-end AI application that analyzes chest X-ray images, predicts possible thoracic diseases, generates medical reasoning for diagnosis, and stores patient scan history for future reference.

The system combines computer vision, language modeling, backend API integration, and persistent cloud storage.

## Features

- User Authentication System
- Chest X-ray Image Upload
- Disease Classification using DenseNet121
- Diagnostic Reasoning Generation using Phi-3 LLM
- Flask Backend API Integration
- MongoDB Atlas Cloud Storage
- External Model Inference Server using Google Colab
- Scan History Persistence

## Architecture

```text
Frontend (HTML/CSS/JS)
          ↓
Flask Backend API
          ↓
Authentication Layer
          ↓
Google Colab Model Server
          ↓
DenseNet121 Disease Detection
          ↓
Phi-3 Reasoning Engine
          ↓
MongoDB Atlas Storage
```

## Tech Stack

Backend:

- Python
- Flask
- Flask-CORS

AI Models:

- PyTorch
- DenseNet121
- Phi-3 Mini

Database:

- MongoDB Atlas

Frontend:

- HTML
- CSS
- JavaScript

## Workflow

1. User uploads chest X-ray image
2. Frontend sends request to Flask backend
3. Flask forwards image to external inference server
4. AI model predicts abnormalities
5. Phi-3 generates diagnostic reasoning
6. Flask stores results in MongoDB Atlas
7. Results displayed to user dashboard

## Future Improvements

- Full cloud deployment
- Patient report PDF generation
- Doctor dashboard
- Model optimization for production inference

## Project Status

Current version supports end-to-end inference pipeline with backend API integration and persistent scan history storage.
