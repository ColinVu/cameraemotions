import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

class SimpleTestDetector:
    def __init__(self):
        # Load OpenCV's pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.cap = None
        self.is_running = False
        self.current_emotion = "No face detected"
        self.emotion_confidence = 0.0
        self.debug_info = "Initializing..."
        
        # Create GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Simple Test - Face & Emotion Detection")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='white')
        style.configure('Emotion.TLabel', font=('Arial', 14), foreground='#ecf0f1')
        style.configure('Confidence.TLabel', font=('Arial', 12), foreground='#bdc3c7')
        style.configure('Debug.TLabel', font=('Arial', 10), foreground='#e74c3c')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Simple Face & Emotion Test", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Video frame
        self.video_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        self.video_frame.pack(pady=10)
        
        self.video_label = tk.Label(self.video_frame, bg='#34495e')
        self.video_label.pack(padx=10, pady=10)
        
        # Debug information frame
        debug_frame = tk.Frame(main_frame, bg='#2c3e50')
        debug_frame.pack(pady=10, fill='x')
        
        # Debug info label
        self.debug_label = ttk.Label(debug_frame, text="Debug: Initializing...", 
                                    style='Debug.TLabel', wraplength=700)
        self.debug_label.pack()
        
        # Emotion display frame
        emotion_frame = tk.Frame(main_frame, bg='#2c3e50')
        emotion_frame.pack(pady=10)
        
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
            self.status_label.config(text="Camera started - Testing detection...")
            
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
        
    def simple_emotion_detection(self, face_region):
        """Simple emotion detection based on facial features"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            
            # Calculate average brightness
            brightness = np.mean(gray)
            
            # Calculate contrast (standard deviation)
            contrast = np.std(gray)
            
            # Simple heuristics for emotion detection
            if brightness > 120:
                if contrast > 30:
                    emotion = "Happy"
                    confidence = min(0.8, (brightness - 100) / 50)
                else:
                    emotion = "Neutral"
                    confidence = 0.6
            elif brightness < 80:
                emotion = "Sad"
                confidence = min(0.7, (80 - brightness) / 40)
            else:
                emotion = "Neutral"
                confidence = 0.5
                
            return emotion, confidence
            
        except Exception as e:
            return "Unknown", 0.0
        
    def process_video(self):
        """Process video frames and detect emotions"""
        frame_count = 0
        detection_count = 0
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                self.debug_info = "Failed to read frame from camera"
                self.root.after(0, self.update_debug_display)
                continue
                
            frame_count += 1
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                self.debug_info = f"Face detected! Frame: {frame_count}"
                
                # Use the largest face
                largest_face = max(faces, key=lambda x: x[2] * x[3])
                x, y, w, h = largest_face
                
                # Draw face detection box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Extract face region for emotion detection
                face_region = frame[y:y+h, x:x+w]
                
                if face_region.size > 0:
                    self.debug_info = f"Face region extracted: {face_region.shape}"
                    
                    # Detect emotion
                    emotion, confidence = self.simple_emotion_detection(face_region)
                    
                    self.current_emotion = emotion
                    self.emotion_confidence = confidence
                    detection_count += 1
                    
                    self.debug_info = f"Emotion detected: {emotion} ({confidence:.1%}) - Detection #{detection_count}"
                    
                    # Update GUI labels
                    self.root.after(0, self.update_emotion_display)
                else:
                    self.debug_info = "Face region is empty or too small"
            else:
                self.current_emotion = "No face detected"
                self.emotion_confidence = 0.0
                self.debug_info = f"No face detected in frame {frame_count}"
                self.root.after(0, self.update_emotion_display)
            
            # Update debug display
            self.root.after(0, self.update_debug_display)
            
            # Convert frame for GUI display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            
            # Resize frame to fit GUI
            display_width = 600
            display_height = 400
            frame_pil = frame_pil.resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            frame_tk = ImageTk.PhotoImage(frame_pil)
            
            # Update video display
            self.root.after(0, lambda: self.video_label.config(image=frame_tk))
            self.root.after(0, lambda: setattr(self.video_label, 'image', frame_tk))
            
            # Control frame rate
            time.sleep(0.05)  # ~20 FPS
            
    def update_emotion_display(self):
        """Update emotion and confidence labels in GUI"""
        self.emotion_label.config(text=f"Emotion: {self.current_emotion}")
        self.confidence_label.config(text=f"Confidence: {self.emotion_confidence:.1%}")
        
    def update_debug_display(self):
        """Update debug information in GUI"""
        self.debug_label.config(text=f"Debug: {self.debug_info}")
        
    def on_closing(self):
        """Handle window closing"""
        self.stop_camera()
        self.root.destroy()
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the simple test detector"""
    print("Starting Simple Test - Face & Emotion Detection...")
    print("This version uses basic facial feature analysis (no DeepFace).")
    
    detector = SimpleTestDetector()
    detector.run()

if __name__ == "__main__":
    main() 