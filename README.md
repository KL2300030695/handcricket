# 🏏 Hand Cricket Game using Hand Gestures (OpenCV + MediaPipe)

This is a real-time **Hand Cricket Game** built using Python, OpenCV, and MediaPipe. You can play cricket by just using your fingers in front of a webcam — no mouse or keyboard needed!

---

## 🚀 Features

- 🖐️ Real-time hand gesture detection using **MediaPipe**
- 🎮 Interactive game flow (Toss → Bat/Bowl → Inning 1 → Inning 2 → Result)
- ✋ Finger-counting logic to detect your "runs"
- 🎯 Target setting and automatic innings switch
- 🧠 Simple AI using random number generation for computer moves
- 🎨 Live feedback, scores, and status shown on webcam feed

---

## 🛠️ Tech Stack

- [Python 3.9+](https://www.python.org/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://google.github.io/mediapipe/)

---

## 📦 Installation

1. ✅ Install **Python 3.9 (64-bit)** if not already installed.
2. 🔁 Create and activate a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/macOS


📦 Install dependencies:

bash
Copy
Edit
pip install opencv-python mediapipe


▶️ Run the game:

bash
Copy
Edit
python handcricket.py
