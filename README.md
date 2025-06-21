# Camera Emotions - Real-time Emotion Detection

A Python application that uses computer vision to detect emotions from facial expressions in real-time using your computer's webcam.

## Features

- **Real-time emotion detection** using your webcam
- **Modern GUI interface** with live video feed
- **Multiple emotion recognition** (Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral)
- **Confidence scoring** for each emotion prediction
- **Face detection** with bounding box visualization
- **Two versions available**: Full version with DeepFace and simple version with basic detection

## Technologies Used

- **Python** - Core programming language
- **OpenCV** - Webcam access and image processing
- **MediaPipe** - Advanced face detection and landmarks
- **DeepFace** - Pre-trained emotion recognition model
- **TensorFlow** - Deep learning framework (via DeepFace)
- **Tkinter** - GUI framework
- **PIL/Pillow** - Image processing for GUI

## Installation

### Prerequisites

- Python 3.8 or higher
- Webcam
- Good lighting for best results

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd cameraemotions
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   **Option 1: Full version (recommended)**
   ```bash
   python emotion_detector.py
   ```
   
   **Option 2: Simple version (faster, less accurate)**
   ```bash
   python simple_emotion_detector.py
   ```

## Usage

1. **Launch the application** - Choose either the full or simple version
2. **Click "Start Camera"** - This will activate your webcam
3. **Position your face** - Make sure your face is clearly visible in the camera
4. **Try different expressions** - The system will detect and display your emotions in real-time
5. **Click "Stop Camera"** - When you're done

## How It Works

### Full Version (`emotion_detector.py`)
- Uses **MediaPipe** for precise face detection
- Employs **DeepFace** with pre-trained models for accurate emotion recognition
- Supports 7 emotion categories with confidence scores
- More accurate but requires more computational resources

### Simple Version (`simple_emotion_detector.py`)
- Uses **OpenCV's Haar Cascade** for face detection
- Implements basic brightness/contrast analysis for emotion detection
- Faster performance but less accurate
- Good for testing or systems with limited resources

## Emotion Categories

The system can detect the following emotions:
- **Happy** - Smiling, positive expressions
- **Sad** - Downward expressions, drooping features
- **Angry** - Frowning, tense facial muscles
- **Surprise** - Raised eyebrows, wide eyes
- **Fear** - Wide eyes, tense expression
- **Disgust** - Nose wrinkling, mouth movements
- **Neutral** - Resting face, no strong emotion

## Troubleshooting

### Common Issues

1. **"Could not open webcam" error**
   - Make sure your webcam is connected and not being used by another application
   - Try restarting your computer
   - Check if your webcam drivers are up to date

2. **Poor emotion detection accuracy**
   - Ensure good lighting conditions
   - Position your face clearly in the camera view
   - Try the full version for better accuracy

3. **Slow performance**
   - Close other applications using the camera
   - Try the simple version for faster performance
   - Ensure you have sufficient RAM and CPU resources

4. **Installation issues**
   - Make sure you have Python 3.8+ installed
   - Try installing dependencies one by one if batch installation fails
   - On Windows, you might need to install Visual C++ build tools

### Performance Tips

- **Good lighting** is crucial for accurate detection
- **Face the camera directly** for best results
- **Keep your face in the center** of the frame
- **Avoid rapid movements** that might confuse the detection
- **Use the full version** for more accurate results

## System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for models and dependencies
- **Camera**: Built-in or external webcam

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving the documentation
- Optimizing the code

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **DeepFace** library for emotion recognition models
- **MediaPipe** for face detection capabilities
- **OpenCV** community for computer vision tools
- **TensorFlow** team for the deep learning framework

---

**Note**: This is a demonstration project. For production use, consider using more robust emotion recognition models and implementing additional security and privacy measures.
