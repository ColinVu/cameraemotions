import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from deepface import DeepFace
import os

class EmotionDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5
        )
        
        self.cap = None
        self.is_running = False
        self.current_emotion = "No face detected"
        self.emotion_confidence = 0.0
        
        # Emotion labels
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        # Create GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Emotion Detection System")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='white')
        style.configure('Emotion.TLabel', font=('Arial', 14), foreground='#ecf0f1')
        style.configure('Confidence.TLabel', font=('Arial', 12), foreground='#bdc3c7')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Real-time Emotion Detection", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Video frame
        self.video_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        self.video_frame.pack(pady=10)
        
        self.video_label = tk.Label(self.video_frame, bg='#34495e')
        self.video_label.pack(padx=10, pady=10)
        
        # Emotion display frame
        emotion_frame = tk.Frame(main_frame, bg='#2c3e50')
        emotion_frame.pack(pady=20)
        
        # Current emotion
        self.emotion_label = ttk.Label(emotion_frame, text="Emotion: No face detected", 
                                      style='Emotion.TLabel')
        self.emotion_label.pack()
        
        # Confidence
        self.confidence_label = ttk.Label(emotion_frame, text="Confidence: 0%", 
                                         style='Confidence.TLabel')
        self.confidence_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="Start Camera", 
                                     command=self.start_camera,
                                     bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                     relief='flat', padx=20, pady=10)
        self.start_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(button_frame, text="Stop Camera", 
                                    command=self.stop_camera,
                                    bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                    relief='flat', padx=20, pady=10, state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        # Status bar
        self.status_label = tk.Label(main_frame, text="Ready to start", 
                                    bg='#34495e', fg='white', font=('Arial', 10))
        self.status_label.pack(pady=10)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def start_camera(self):
        """Start the webcam and emotion detection"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open webcam")
            
            self.is_running = True
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.status_label.config(text="Camera started - Detecting emotions...")
            
            # Start video processing in a separate thread
            self.video_thread = threading.Thread(target=self.process_video)
            self.video_thread.daemon = True
            self.video_thread.start()
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            
    def stop_camera(self):
        """Stop the webcam and emotion detection"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Camera stopped")
        
        # Clear video display
        self.video_label.config(image='')
        
    def process_video(self):
        """Process video frames and detect emotions"""
        frame_count = 0
        emotion_detection_count = 0
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            frame_count += 1
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            results = self.face_detection.process(rgb_frame)
            
            if results.detections:
                for detection in results.detections:
                    # Draw face detection box
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                           int(bboxC.width * iw), int(bboxC.height * ih)
                    
                    cv2.rectangle(frame, bbox, (0, 255, 0), 2)
                    
                    # Extract face region for emotion detection
                    face_region = frame[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                    
                    if face_region.size > 0:
                        # Detect emotion using DeepFace
                        try:
                            emotion_result = DeepFace.analyze(face_region, 
                                                           actions=['emotion'], 
                                                           enforce_detection=False)
                            
                            if isinstance(emotion_result, list):
                                emotion_result = emotion_result[0]
                            
                            emotion = emotion_result['dominant_emotion']
                            confidence = max(emotion_result['emotion'].values())
                            
                            self.current_emotion = emotion.capitalize()
                            self.emotion_confidence = confidence
                            emotion_detection_count += 1
                            
                            # Update GUI labels
                            self.root.after(0, self.update_emotion_display)
                            
                        except Exception as e:
                            print(f"Emotion detection error: {e}")
                            self.current_emotion = "Detection failed"
                            self.emotion_confidence = 0.0
                            self.root.after(0, self.update_emotion_display)
                    else:
                        self.current_emotion = "Face too small"
                        self.emotion_confidence = 0.0
                        self.root.after(0, self.update_emotion_display)
            else:
                self.current_emotion = "No face detected"
                self.emotion_confidence = 0.0
                self.root.after(0, self.update_emotion_display)
            
            # Convert frame for GUI display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            
            # Resize frame to fit GUI
            display_width = 640
            display_height = 480
            frame_pil = frame_pil.resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            frame_tk = ImageTk.PhotoImage(frame_pil)
            
            # Update video display
            self.root.after(0, lambda: self.video_label.config(image=frame_tk))
            self.root.after(0, lambda: setattr(self.video_label, 'image', frame_tk))
            
            # Control frame rate
            time.sleep(0.03)  # ~30 FPS
            
    def update_emotion_display(self):
        """Update emotion and confidence labels in GUI"""
        self.emotion_label.config(text=f"Emotion: {self.current_emotion}")
        self.confidence_label.config(text=f"Confidence: {self.emotion_confidence:.1%}")
        
    def on_closing(self):
        """Handle window closing"""
        self.stop_camera()
        self.root.destroy()
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the emotion detector"""
    print("Starting Emotion Detection System...")
    print("Make sure you have a webcam connected and good lighting for best results.")
    
    detector = EmotionDetector()
    detector.run()

if __name__ == "__main__":
    main() 