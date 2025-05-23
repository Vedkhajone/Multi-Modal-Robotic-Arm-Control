# 🤖 Multi-Modal Robotic Arm Control

A Python-based simulation and control interface for a robotic arm using multiple input modalities—including GUI interaction and (planned) real-time hand motion tracking. Designed to simulate and prototype intelligent robotic arm control for embedded or software-based applications.

## 📸 Demo

---

## 🧠 Project Description

This project allows users to:
- **Control a robotic arm** using inverse kinematics (IK) via a point-and-click GUI.
- **Simulate servo movements** in a `matplotlib` environment.
- **Send angles to ESP32** over serial to control physical servos (for embedded deployment).
- Demonstrates integration of computer vision, robotics, and embedded systems.
- *(Planned)* **Track real-time hand motion** using OpenCV + Mediapipe.

---

## 🚀 Features

- ✅ Inverse Kinematics (3-DOF)
- ✅ Matplotlib-based interactive GUI
- ✅ ESP32 integration with servo control
- ✅ Multi-modal input support (GUI click, future: hand tracking)
- ✅ Real-time animated arm visualization
- 🔄 *(Planned)* Hand motion tracking via webcam

---

## 🛠️ Technologies Used

- Python 
- Matplotlib
- NumPy
- PySerial (for ESP32 communication)
- ESP32 (for servo control)

---

## 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/Vedkhajone/Multi-Modal-Robotic-Arm-Control.git
cd Multi-Modal-Robotic-Arm-Control
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Simulation
To launch the arm GUI:
```bash
python main_ik_gui.py
```
### 4.Connect to ESP32
Flash this Arduino code to your ESP32:


## 📂 Project Structure

📁 Multi-Modal-Robotic-Arm-Control/
├── robotic_arm.py            # Core arm logic (IK, kinematics)
├── main_ik_gui.py            # Main GUI for arm simulation
├── hand_control.py           # (Planned) Hand-tracking input
├── esp32_arduino_code.ino    # Servo control for ESP32
├── requirements.txt          # Python dependencies
└── README.md                 # This file

## 🧠 Future Ideas
- 👋 Implement hand-tracking module using Mediapipe
- 🗣️ Add voice command integration
- 🖐️ Integrate Leap Motion or gesture sensors
- 🤖 Upgrade to 6-DOF arm model
- 🎮 Add joystick/gamepad support
- 🌐 Web-based remote control

## 🤝 Contribution
Contributions, issues, and feature requests are welcome!
Please open a pull request or create an issue to get started.

## 📜 License
MIT License © Vedhanshu Khajone – 2025


