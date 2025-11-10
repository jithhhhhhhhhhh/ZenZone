import cv2
import mediapipe as mp
import numpy as np
import json
import os
from gtts import gTTS
import pygame
import tempfile
import warnings

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.audio_files = {}
        self.pose_configs = {}  # Cache for loaded pose configurations
        self._init_audio_system()
    
    def _init_audio_system(self):
        """Initialize audio system with fallback options"""
        try:
            from pydub import AudioSegment
            from pydub.playback import play
            self._has_pydub = True
        except ImportError:
            self._has_pydub = False
            warnings.warn("Pydub not available, using pygame for audio")
        
        pygame.mixer.init()
    
    def get_pose_description(self, pose_name):
        """Get description text for a pose"""
        descriptions = {
            "tadasana": "Tadasana or Mountain Pose is the foundation of all standing poses. "
                       "It improves posture, strengthens thighs and ankles, and reduces flat feet. "
                       "Stand tall with feet together, shoulders relaxed, and arms by your sides.",
            
            "vrikshasana": "Vrikshasana or Tree Pose improves balance and focus. "
                          "Stand on one leg, place the other foot on your inner thigh or calf, "
                          "and bring your hands to prayer position at your chest.",
            
            "adho_mukha_svanasana": "Adho Mukha Svanasana or Downward Dog stretches the hamstrings, "
                                   "calves, and spine while strengthening arms and legs. "
                                   "Form an inverted V-shape with your body, hands and feet on the mat.",
            
            "bhujangasana": "Bhujangasana or Cobra Pose strengthens the spine and opens the chest. "
                           "Lie on your stomach, place hands under shoulders, and lift your chest "
                           "while keeping hips on the mat.",
            
            "trikonasana": "Trikonasana or Triangle Pose stretches legs, hips and spine. "
                          "Stand with legs wide apart, reach one hand to your foot and the other to the sky, "
                          "creating a straight line from hand to hand.",
            
            "virabhadrasana_ii": "Virabhadrasana II or Warrior II builds stamina and concentration. "
                                "Stand with legs wide apart, turn one foot out, bend the front knee, "
                                "and stretch arms parallel to the floor."
        }
        return descriptions.get(pose_name, "This is a yoga pose. Follow the on-screen guidance.")
    
    def load_pose_config(self, pose_name):
        """Load yoga pose configuration from JSON file"""
        if pose_name in self.pose_configs:
            return self.pose_configs[pose_name]
            
        config_path = os.path.join('yoga_poses', f'{pose_name}.json')
        try:
            with open(config_path) as f:
                config = json.load(f)
                self.pose_configs[pose_name] = config
                return config
        except FileNotFoundError:
            raise ValueError(f"Pose configuration not found: {pose_name}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in pose configuration: {pose_name}")
    
    def speak_feedback(self, text):
        """Text-to-speech feedback with error handling"""
        if not text.strip():
            return
            
        try:
            if text not in self.audio_files:
                tts = gTTS(text=text, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    tts.save(fp.name)
                    self.audio_files[text] = fp.name
            
            self._play_audio(self.audio_files[text])
        except Exception as e:
            print(f"Audio playback failed: {str(e)}")
            print(f"Feedback: {text}")
    
    def _play_audio(self, filepath):
        """Play audio using available backend"""
        if self._has_pydub:
            try:
                from pydub import AudioSegment
                from pydub.playback import play
                sound = AudioSegment.from_mp3(filepath)
                play(sound)
                return
            except:
                pass
        
        # Fallback to pygame
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    def detect_pose(self, image, pose_config):
        """Detect and analyze yoga pose"""
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        
        feedback = ""
        accuracy = 0
        
        if results.pose_landmarks and pose_config:
            accuracy, feedback = self.analyze_pose(
                results.pose_landmarks.landmark, 
                pose_config
            )
        
        return image, accuracy, feedback
    
    def analyze_pose(self, landmarks, pose_config):
        """Analyze pose against configuration"""
        required_landmarks = pose_config.get('required_landmarks', [])
        visible_landmarks = 0
        feedback = []
        
        for landmark in required_landmarks:
            if hasattr(self.mp_pose.PoseLandmark, landmark):
                if landmarks[getattr(self.mp_pose.PoseLandmark, landmark)].visibility > 0.5:
                    visible_landmarks += 1
                else:
                    feedback.append(f"Adjust your {landmark.replace('_', ' ')}")
            else:
                print(f"Warning: Invalid landmark {landmark} in pose config")
        
        accuracy = (visible_landmarks / len(required_landmarks)) * 100 if required_landmarks else 0
        return accuracy, ". ".join(feedback) if feedback else "Good form!"