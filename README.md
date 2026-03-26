# 🎨 Air Canvas Premium – AI Powered Virtual Painter

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge\&logo=python\&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg?style=for-the-badge\&logo=opencv\&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg?style=for-the-badge\&logo=google\&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red.svg?style=for-the-badge)

---

## 📌 About Project

**Air Canvas Premium** is an AI-powered virtual drawing application built with
Computer Vision, OpenCV and Google MediaPipe.

You can draw in the air using only your hand gestures without touching the screen.

This project includes advanced UI logic, hitbox algorithms and real-time gesture tracking.

✔ Safe UI Zones
✔ Aim Assist Hitbox
✔ Dynamic Brush Size
✔ Shape Preview Engine
✔ Layered Interface System
✔ Real-time Hand Tracking

---

## ✨ Features

### 🛡 Safe Zone System

Drawing automatically stops when the cursor enters menu areas.

### 🎯 Aim Assist Hitbox

Buttons have buffer zone for smoother selection.

### 📐 Dynamic Brush Size

Brush size changes with finger distance.

Range:

5px → 50px

### 🎨 Layered UI System

* UI always on top
* Canvas below
* Transparent panels
* Modern flat design

### 🔳 Shape Preview Engine

* Rectangle
* Circle
* Live preview
* Smart placement

---

## 🕹 Gesture Controls

| Gesture          | Mode  | Description    |
| ---------------- | ----- | -------------- |
| ☝ Index Finger   | Draw  | Free drawing   |
| ✌ Two Fingers    | Hover | Menu selection |
| 🤏 Three Fingers | Size  | Brush size     |
| 🛑 Clean Button  | Reset | Clear canvas   |

---

## 📦 Requirements

* Python 3.10 or 3.11 recommended
* Webcam required

---

## ⚙ Installation

### 1. Clone repo

```
git clone https://github.com/ardairmk55/air_canvas
cd air_canvas
```

### 2. Create virtual environment

Windows

```
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

If requirements.txt yoksa:

```
pip install opencv-python mediapipe numpy
```

---

## ▶ Run

```
python air_canvas.py
```

Press Q to exit.

---

## 📂 Project Structure

```
air_canvas/
│
├── air_canvas.py
├── requirements.txt
├── README.md
├── .gitignore
└── demo/
    └── demo.gif
```

---

## 🧠 Technologies

* OpenCV
* MediaPipe
* NumPy
* Computer Vision
* Hand Tracking
* Gesture Recognition
* UI Layer System
* Hitbox Algorithm

---

## 📷 Demo

Add gif here

/demo/demo.gif

---

## 👨‍💻 Developer

Arda Irmak
Gümüşhane University
Computer Programming

GitHub:
https://github.com/ardairmk55

---

## 📄 License

MIT License

Free to use, modify and share.
