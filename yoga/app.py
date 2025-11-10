import streamlit as st
import cv2
import numpy as np
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
from pose_utils import PoseDetector
import tempfile
import os

# Initialize pose detector
@st.cache_resource
def get_pose_detector():
    return PoseDetector()

def main():
    st.set_page_config(
        page_title="Yoga AI Coach",
        page_icon="🧘",
        layout="wide"
    )
    
    # Initialize session state
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'coins': 0,
            'sessions': [],
            'current_session': None
        }
    
    pose_detector = get_pose_detector()
    
    # Sidebar navigation
    st.sidebar.title("🧘 Yoga AI Coach")
    page = st.sidebar.radio("Menu", ["🏠 Home", "💪 Practice", "📊 Dashboard"])
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "💪 Practice":
        show_practice_page(pose_detector)
    elif page == "📊 Dashboard":
        show_dashboard_page()

def show_home_page():
    st.title("Welcome to Yoga AI Coach! 🙏")
    st.markdown("""
    <style>
    .welcome-text {
        font-size: 18px;
        line-height: 1.6;
    }
    </style>
    <div class="welcome-text">
    Namaste! Our Yoga AI Coach helps you perfect your yoga practice with real-time feedback. 
    Whether you're a beginner or an experienced practitioner, our AI-powered system will 
    guide you toward proper alignment and form.
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://cms-artifacts.artlist.io/content/motion_array/1617102/6_Yoga_Poses_Illustrations_high_resolution_preview_1617102.jpg?Expires=2037539736399&Key-Pair-Id=K2ZDLYDZI2R1DF&Signature=biyFtxd-KI0eqAX9sLdWhsYf~KhC7vsfGgD31MQkwWy9eYMuRRpsZKDEUeIgpzU~tbVNjm5PP84WCFInyi46pgabjofPZob8ZS9yIqg1xMOpY0zuJeKoEf1sBfKS-GGf~omG-JwTd0N967iuzG2wvXpzIca50opuv3WA7aPPd9eZzaixSJzPJTvJguLF41vdaolvcpNMIF9E8QmoXt~88jm558PQIT7VQPWMsSKeooTZCTfEYfIQKOiDdZKWJJOx6WnmpHGQLlPBR7J23Lva29xRJ5GLVNNfqTOK8T3evZiodRPQd11WRTZkM7VzO7suaYIu6Tvu80QZPZ3jsHk-Iw__", 
             use_container_width=True)
    
    st.markdown("""
    ### **Perfect Your Yoga Poses with AI Feedback**
    - Real-time pose correction 🎯
    - Multiple supported yoga poses 🧘‍♂️
    - Video upload & webcam support 📹
    - Earn coins for practice 🪙
    
    ### Getting Started
    1. Select **Practice** from the menu
    2. Choose a yoga pose you want to work on
    3. Use your webcam or upload a video
    4. Get instant feedback on your form
    5. Track your progress in the Dashboard
    """)

def show_practice_page(pose_detector):
    st.title("Practice Yoga")
    
    # Pose selection with descriptions and images
    pose_options = {
    "tadasana": {
        "name": "Tadasana (Mountain Pose)",
        "description": "The foundation of all standing poses, Tadasana improves posture, strengthens thighs and ankles, and reduces flat feet.",
        "image_url": "https://www.yogaclassplan.com/wp-content/uploads/2021/06/mountain.jpg"
    },
    "vrikshasana": {
        "name": "Vrikshasana (Tree Pose)",
        "description": "This balancing pose strengthens legs, improves focus, and helps develop balance and stability in the legs.",
        "image_url": "https://www.yogaclassplan.com/wp-content/uploads/2021/01/34-treepose.jpg"
    },
    "adho_mukha_svanasana": {
        "name": "Adho Mukha Svanasana (Downward Dog)",
        "description": "A rejuvenating pose that stretches hamstrings, calves, and spine while strengthening arms and legs.",
        "image_url": "https://www.yogaclassplan.com/wp-content/uploads/2021/06/downward-facingdog.png"
    },
    "bhujangasana": {
        "name": "Bhujangasana (Cobra Pose)",
        "description": "This gentle backbend strengthens the spine, opens the chest and shoulders, and helps relieve stress and fatigue.",
        "image_url": "https://www.yogaclassplan.com/wp-content/uploads/2021/06/Bhujangasana-Cobra-Pose.png"
    },
    "trikonasana": {
        "name": "Trikonasana (Triangle Pose)",
        "description": "This standing pose stretches legs, hips and spine while stimulating abdominal organs and improving digestion.",
        "image_url": "https://www.yogaclassplan.com/wp-content/uploads/2021/01/27-triangle.jpg"
    },
    "virabhadrasana_ii": {
        "name": "Virabhadrasana II (Warrior II)",
        "description": "A powerful standing pose that strengthens legs and arms, increases stamina, and improves balance and concentration.",
        "image_url": "https://www.yogaclassplan.com/wp-content/uploads/2021/01/31-warrior-2.jpg"
    }
    }

    
    selected_pose_key = st.selectbox(
        "Choose a Yoga Pose",
        options=list(pose_options.keys()),
        format_func=lambda x: pose_options[x]["name"]
    )
    
    # Display pose description and reference image
    st.markdown(f"**About {pose_options[selected_pose_key]['name']}**")
    st.markdown(pose_options[selected_pose_key]['description'])
    
    col1, col2 = st.columns(2)
    with col1:
        try:
            st.image(pose_options[selected_pose_key]['image_url'], 
                    caption=f"Reference: {pose_options[selected_pose_key]['name']}",
                    use_container_width=True)
        except:
            st.error("Could not load pose reference image. Please check your internet connection.")
            st.markdown(f"[Reference Image Link]({pose_options[selected_pose_key]['image_url']})")
    
    try:
        pose_config = pose_detector.load_pose_config(selected_pose_key)
    except ValueError as e:
        st.error(str(e))
        return
    
    # Input selection
    input_option = st.radio("Input Source", ["Webcam", "Upload Video"])
    
    cap = None
    if input_option == "Webcam":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not open webcam. Please check permissions.")
            return
    else:
        uploaded_file = st.file_uploader("Upload a Yoga Video", type=["mp4", "mov"])
        if uploaded_file:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                cap = cv2.VideoCapture(tmp_file.name)
    
    # Initialize session state
    if 'practice_active' not in st.session_state:
        st.session_state.practice_active = False
    
    # Start/Stop buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Practice") and cap:
            st.session_state.practice_active = True
            st.session_state.start_time = time.time()
            st.session_state.pose_description_played = False
            st.session_state.current_session = {
                'pose': pose_options[selected_pose_key]["name"],
                'start_time': datetime.now(),
                'accuracy_history': []
            }
    
    with col2:
        if st.button("Stop Practice"):
            st.session_state.practice_active = False
            if cap:
                cap.release()
            if 'current_session' in st.session_state:
                save_session_data()
    
    # Display area
    stframe = st.empty()
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    # Main processing loop
    if st.session_state.get('practice_active') and cap:
        process_video_feed(pose_detector, pose_config, cap, stframe, stats_col1, stats_col2, stats_col3, selected_pose_key)

def process_video_feed(pose_detector, pose_config, cap, stframe, stats_col1, stats_col2, stats_col3, selected_pose_key):
    try:
        # Play initial pose description only once
        if not st.session_state.get('pose_description_played'):
            description = pose_detector.get_pose_description(selected_pose_key)
            pose_detector.speak_feedback(description)
            st.session_state.pose_description_played = True
            time.sleep(5)  # Give user time to get into position
            
        while st.session_state.practice_active and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("Video stream ended")
                st.session_state.practice_active = False
                break
            
            # Process frame
            frame = cv2.flip(frame, 1)
            frame, accuracy, feedback = pose_detector.detect_pose(frame, pose_config)
            
            # Update session
            st.session_state.current_session['accuracy_history'].append({
                'time': time.time() - st.session_state.start_time,
                'accuracy': accuracy
            })
            
            # Display
            stframe.image(frame, channels="BGR")
            
            # Stats 
            with stats_col1:
                st.metric("⏱️ Time", f"{int(time.time() - st.session_state.start_time)}s")
            with stats_col2:
                st.metric("🎯 Accuracy", f"{accuracy:.1f}%")
            with stats_col3:
                st.text("🗣️ Feedback")
                st.write(feedback)
                if accuracy < 70 and feedback:
                    pose_detector.speak_feedback(feedback)
            
            time.sleep(0.1)
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
    finally:
        if cap and cap.isOpened():
            cap.release()
        st.session_state.practice_active = False
        st.session_state.pose_description_played = False  # Reset for next session

def save_session_data():
    duration = time.time() - st.session_state.start_time
    avg_accuracy = np.mean(
        [x['accuracy'] for x in st.session_state.current_session['accuracy_history']]
    ) if st.session_state.current_session['accuracy_history'] else 0
    
    # Reward coins (1 per minute)
    coins_earned = int(duration // 60)
    st.session_state.user_data['coins'] += coins_earned
    
    # Save session
    st.session_state.user_data['sessions'].append({
        'pose': st.session_state.current_session['pose'],
        'duration': duration,
        'accuracy': avg_accuracy,
        'date': datetime.now(),
        'coins_earned': coins_earned
    })
    
    st.success(f"Session completed! You earned {coins_earned} coins.")

def show_dashboard_page():
    st.title("Your Progress")
    
    if not st.session_state.user_data['sessions']:
        st.info("No sessions yet. Start practicing!")
        return
    
    df = pd.DataFrame(st.session_state.user_data['sessions'])
    df['date'] = pd.to_datetime(df['date'])
    
    # Stats cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🪙 Total Coins", st.session_state.user_data['coins'])
    with col2:
        st.metric("🧘 Total Sessions", len(df))
    with col3:
        st.metric("⏳ Total Time", f"{df['duration'].sum() / 60:.1f} mins")
    
    # Charts
    st.subheader("Progress Over Time")
    fig1 = px.line(df, x='date', y='accuracy', color='pose', title="Accuracy Trend")
    st.plotly_chart(fig1)
    
    fig2 = px.bar(df.groupby('pose')['duration'].sum().reset_index(), 
                 x='pose', y='duration', title="Time Spent per Pose")
    st.plotly_chart(fig2)

if __name__ == "__main__":
    main()