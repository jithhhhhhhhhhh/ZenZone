# ZenZone
Problems with mental health are
increasing in this digital era specially in the working
sector and students. We recommend ZenZone an online
tool for mental wellness incorporating deep learning, AI
and interactive design in order to assist users cognitively
and emotionally as the remedy to solve the mentioned
issues. Mental health AI-based chatbot, music
recommendations based on emotions, stress-relieving
games, yoga therapy, inspirational quotes and wellness
articles are six features of ZenZone that are intertwined.
The Spotify API is leveraged by the emotion recognition
module to generate mood based music that is linked with
the facial expressions as classified by the CNN model. The
chatbot provides an instant mental health service and
designed with LangChain and a Large language model.
ZenZone is made with HTML, CSS, Javascript and
Streamlit and provides a enjoyable like user interface.
Following positive early tests, it is a useful online digital
tool for promoting healthy psychological wellbeing and
creating healthy behaviours, reducing stress and
improving concentration.



SYSTEM ARCHITECTURE AND DESIGN

ZenZone is designed with modular and scalable architecture,
which can be developed independently, maintained with ease
and expanded in the future. The application is created using a
blend of current frontend and backend technologies to provide a
smooth and engaging user experience. The technologies are:
• Frontend: Designed using HTML, CSS, JavaScript and
Bootstrap for responsive and user-friendly web
interfaces.
• Backend: Streamlit-powered, which manages real-time
UI interactions like webcam usage, file upload and live
emotion detection output.
• AI & ML Models: A deep learning model based on CNN
is utilized for facial emotion detection, along with
OpenCV and Haarcascade for face detection and
preprocessing.
• Music Recommendation: The Spotify API is utilized to
recommend and play music based on the identified
emotional state.
• Mental Health Chatbot: A smart chatbot developed on a
Large Language Model (LLM) and LangChain
framework with motivational guidance and mental health
discussions.
• Yoga Pose Correction: Created with MediaPipe, this
module examines user poses in real time, detects errors
and provides corrective hints to correct posture and
reduce stress.

Every module runs independently but speaks to each other
seamlessly via the Streamlit framework, providing a
responsive and real-time user interface. The system is scalable
enough to accommodate future enhancements such as
gamified objectives, mobile application deployment and other
emotional support features.

A. User Interface
ZenZone app has a clean and neat user interface, written with
simplicity in mind. It was developed using HTML, CSS,
JavaScript and Bootstrap, taking care to ensure simplicity of
use by providing effortless access to the different features of
the app.Whether it's the emotion-based music
recommendations, mental health chatbot or yoga pose
correction, the interface seamlessly presents these tools in a
way that's both visually appealing and user-friendly. The
responsive nature of the design guarantees seamless access
across devices, providing a good experience to everyone.

B. Application logic
The core of ZenZone's functionality is within its application
logic. With Streamlit, the app provides users with interactivity
with live features like image upload, playing customized
music and getting feedback on their yoga pose. The backend
logic integrates multiple features in an effortless manner, such
as emotion-driven music suggestions, mental health chatbot
conversations, stress-relief games, articles reading and
motivational quotes sharing. The reasoning behind this is to
make sure that all of these components play harmoniously
together, controlling the flow between them to present a
seamless user experience. Whether a user uses the chatbot,
emotion recognition or plays interactive games, the app
promises a seamless, reactive experience that is refined to the
user's mind, emotional and physical health needs in real-time.

C. AI/ML Model
ZenZone incorporates sophisticated AI/ML models to enrich
user interaction. Emotion recognition model is constructed
with a CNN which identifies facial emotions through webcam.
MediaPipe is also utilized for the correction of yoga pose
which offering real-time feedback on the posture of the user.
LLM chatbot developed with LangChain which provides
personalized emotional support, making it an exhaustive,
reactive system.

D. Integration services
ZenZone natively incorporates a variety of services to enable
an integrated experience. The Spotify API provides music
suggestions based on emotions, whereas LangChain provides
real-time conversation with the chatbot. MediaPipe is also
integrated with the app for the detection of yoga poses,
maintaining smooth communication among all features to
provide the best possible user experience.

E. Auxiliary Modules
Auxiliary modules consist of stress-relief games like Car
Fighter, Brick Breaker and Tic-Tac-Toe, which are
entertaining and soothing activities for users. The reading
center offers a repository of motivational articles, audiobooks
and books to aid mental enrichment. The quotes sharing
function also shares daily inspirational quotes which can be
shared or saved for emotional enrichment.

METHODOLOGY

A. Music Recommendation Module
The system uses a deep learning approach to recommend
personalized music based on the facial emotions. Users can
upload an image or use a webcam to capture their facial
emotion. The input is processed using OpenCV and
Haarcascade to detect faces and a CNN model trained on the
emotion datasets which classifies the emotion. Detected
emotions are mapped to curated Spotify playlists via the
Spotify API. Streamlit provides the user interface. The system
delivers realtime mood based music suggestions in an
engaging UI and aiming to improve user emotional wellbeing
through music therapy.

B. Chatbot
The chatbot leverages LangChain and a locally hosted
LLaMA-2 language model to provide real-time mental
health support. Healthcare-related PDF documents are
loaded, split using a recursive text splitter and embedded
with HuggingFace sentence transformers. These are stored in
a FAISS vector database for efficient semantic retrieval. A
ConversationalRetrievalChain is employed to manage the
dynamic queries with context preservation through
ConversationBufferMemory. The frontend developed using
Streamlit which provides a seamless chat experience. Users
can ask questions and the model retrieves information from
the document base to provide smart, context-aware replies
and supporting emotional health through conversational AI.

C. Yoga Therapy
Yoga AI Coach is a smart web app developed with
Streamlit that teaches yoga for the users with instant
feedback. Based on webcam or video input, it recognizes and
scores yoga poses with the assistance of a pose detection
model. Users can choose from multiple yoga poses. Then get
immediate audio and visual feedback. Users can monitor their
accuracy and improvement over time. The application
rewards the users with coins for finished sessions and
offers detailed dashboards with metrics and charts. It
integrates pose correction, motivational and data
visualization to enable users to enhance their yoga practice
effectively and efficiently from the convenience of home.
Through combining pose estimation with a web based
interface, the module enhances access to guided yoga,
aiding users in stress management as well as physical wellbeing from the comfort of their homes.

D. Stress Relief Games
The Stress Relief Games module provides interactive
browser based exercises which induce relaxation and
mental reset. These consist of light games like puzzles,
breathing and concentration exercises intended to eliminate
mental tiredness and instill a sense of accomplishment. The
games are minimalistic and free from distractions and are
ideal for brief pauses. They aid in helping the users anxious
energy into relaxing activities, enhance general mood and
attention. By adding gaming as a wellness application,
ZenZone maintains an equilibrium of fun and functionality
with promoting mental refreshment without extra
downloads or configuration.

E. Quotes Sharing
The Quotes Sharing module provides a curated set of
inspirational and motivational quotes to the users. These are
not AI-moderated but carefully curated to encourage
positivity, resilience and mindfulness. Users can go through
these positive messages and share their preferred ones
directly on Twitter with one click. This module serves as a
digital source of encouragement, enabling users to encourage
themselves or others. Its simplicity and social sharing features
make it a tiny but useful piece in preserving emotional wellbeing in the app.

F. Reading Articles
The Reading Articles module offers access to carefully
selected wellness material such as audiobooks, podcasts and
written articles. The content is centered on mental health,
self-development mindfulness and motivation. The module
invites users to reflect mindfully and acquire skills for
emotional control. Whether listening to a soothing podcast
or reading a concentrated article, users are able to ingest
knowledge at their own pace. The variety of content format
accommodates different learning styles and preferences and
thus serves as an excellent source of selfguided learning and
stress management.
