🕹️ Motion-Controlled Pong

A fun Python project that combines computer vision and game development — play Pong using your hand movements instead of a keyboard or mouse!

This project uses:

🧮 NumPy for efficient math and collision logic

📷 OpenCV for real-time hand or color object tracking

🎮 Pygame for game visuals, movement, and scoring

🎯 Features

Control the Pong paddle using your webcam

Real-time color-based hand/object detection

Smooth gameplay powered by NumPy vectors

Simple AI opponent

Adjustable difficulty and color detection range

🧰 Requirements

Python 3.8+

Libraries:

pip install pygame numpy opencv-python


(Optional: use opencv-python-headless if you face GUI issues)

⚙️ How to Run

Clone or download this repository

git clone https://github.com/yourusername/motion-controlled-pong.git
cd motion-controlled-pong


Create a virtual environment (recommended)

python -m venv pongenv
pongenv\Scripts\activate   # (Windows)
source pongenv/bin/activate  # (Mac/Linux)


Install dependencies

pip install -r requirements.txt


(or install manually as shown above)

Run the game

python motion_pong.py

🎮 Controls
Action	How
Move paddle	Move your colored object / hand up or down in front of the webcam
Quit game	Press the X button or Esc key in the OpenCV window
⚙️ Adjusting Color Detection

To match your object color:

Open motion_pong.py

Edit these HSV values:

lower_color = np.array([90, 100, 100])  # Lower HSV bound
upper_color = np.array([130, 255, 255]) # Upper HSV bound


You can use a color picker (like colorpicker.me
) to find your HSV range.
Blue works best for testing (try a blue pen cap, glove, or paper).

🧠 Future Improvements

Replace color tracking with MediaPipe Hands for real hand tracking

Add sound effects and scoreboard

Multiplayer mode (two webcams or two-color tracking)

Add difficulty scaling (ball speed increases over time)

💡 Concept

This project demonstrates how computer vision (OpenCV) and game logic (Pygame) can merge into an interactive, real-time experience — perfect for beginners exploring AI + game dev crossover projects.

🧑‍💻 Author
Huda (Me)
Made with ❤️ using Python, NumPy, OpenCV, and Pygame.

📸 Demo Preview

🖐️ Move your hand — 🎾 The paddle follows your motion in real time!
