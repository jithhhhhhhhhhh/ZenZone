import os
import numpy as np
import tensorflow as tf
import cv2 
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ========== Spotify Authentication ==========
SPOTIFY_CLIENT_ID = "c59e08cd48f642dfb71156e6d67b2d82"
SPOTIFY_CLIENT_SECRET = "4bf955e31746490890b10ac17d4859bb"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# ========== Load Haarcascade for Face Detection ==========
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ========== Load Trained Model ==========
model = tf.keras.models.load_model("facial_expression_model.h5")
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# ========== Emotion Detection Function ==========
def detect_emotion(frame, model):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    detected_emotions = []
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = np.expand_dims(np.expand_dims(roi_gray, -1), 0)
        prediction = model.predict(roi_gray)
        max_index = int(np.argmax(prediction))
        
        # Emotion mapping
        emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
        detected_emotions.append(emotion_dict[max_index])
    
    return detected_emotions

# ========== Spotify Playlist IDs for Each Emotion ==========
emotion_playlists = {
    "Angry": "37i9dQZF1DX3rxVfibe1L0",  # Calm Vibes
    "Disgust": "37i9dQZF1DX3rxVfibe1L0",  # Calm Vibes
    "Fear": "37i9dQZF1DX3rxVfibe1L0",  # Calm Vibes
    "Happy": "37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
    "Neutral": "37i9dQZF1DX4WYpdgoIcn6",  # Chill Hits
    "Sad": "37i9dQZF1DX3rxVfibe1L0",  # Calm Vibes
    "Surprised": "37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
}

# ========== Custom CSS for Styling ==========
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;  /* Black background */
        color: #ffffff;  /* White text */
    }
    .stButton>button {
        background-color: #ff0000;  /* Red button */
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #cc0000;  /* Darker red on hover */
    }
    .stFileUploader>div>div>div>button {
        background-color: #ff0000;  /* Red button */
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }
    .stFileUploader>div>div>div>button:hover {
        background-color: #cc0000;  /* Darker red on hover */
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1e90ff;  /* Blue headings */
    }
    .stMarkdown iframe {
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);  /* Red shadow */
    }
    .stSuccess {
        background-color: #1e90ff;  /* Blue success message */
        color: white;
        border-radius: 12px;
        padding: 10px;
    }
    .stWarning {
        background-color: #ff0000;  /* Red warning message */
        color: white;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== Streamlit App ==========
st.title("\U0001F3AD Emotion-Based Music Recommendation \U0001F3B5")
st.markdown("Welcome to **MoodTunes**! Upload an image or use your camera to detect your emotion, and we'll recommend the perfect playlist for you. 🎶")

# Option to Upload Image
st.subheader("📷 Upload an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    emotions = detect_emotion(frame, model)
    if emotions:
        detected_emotion = emotions[0]
        st.success(f"🎭 Detected Emotion: **{detected_emotion}**")

        # Fetch the corresponding Spotify playlist for the detected emotion
        playlist_id = emotion_playlists.get(detected_emotion, "37i9dQZF1DX4WYpdgoIcn6")  # Default: Chill Hits
        embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator"

        # Display the embedded Spotify playlist
        st.subheader(f"🎶 Recommended Playlist for {detected_emotion}:")
        st.markdown(
            f"""
            <iframe
                style="border-radius: 12px"
                src="{embed_url}"
                width="100%"
                height="380"
                frameBorder="0"
                allowfullscreen=""
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                loading="lazy">
            </iframe>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠ No face detected. Try again with a clearer image.")

# Option to Scan Emotion from Camera
st.subheader("📸 Scan Emotion from Camera")
if st.button("Click here to scan your emotion"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        emotions = detect_emotion(frame, model)
        if emotions:
            detected_emotion = emotions[0]
            st.success(f"🎭 Detected Emotion: **{detected_emotion}**")

            # Fetch the corresponding Spotify playlist for the detected emotion
            playlist_id = emotion_playlists.get(detected_emotion, "37i9dQZF1DX4WYpdgoIcn6")  # Default: Chill Hits
            embed_url = f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator"

            # Display the embedded Spotify playlist
            st.subheader(f"🎶 Recommended Playlist for {detected_emotion}:")
            st.markdown(
                f"""
                <iframe
                    style="border-radius: 12px"
                    src="{embed_url}"
                    width="100%"
                    height="380"
                    frameBorder="0"
                    allowfullscreen=""
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy">
                </iframe>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠ No face detected. Try again.")