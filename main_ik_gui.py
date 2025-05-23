import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from robotic_arm import RoboticArm
import numpy as np
from scipy.optimize import minimize
import serial



# === Serial Setup ===
esp32 = serial.Serial('COM5', 115200, timeout=1)


# === Globals ===
arm = RoboticArm(num_joints=3)
target = None  # (x, y)
current_angles = arm.angles.copy()

# === GUI ===
root = tk.Tk()
root.title("IK-Controlled Robotic Arm")

frame = ttk.Frame(root)
frame.grid(row=0, column=0)

# === Matplotlib setup ===
fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()
angle_label = ttk.Label(frame, text="Angles: [0, 0, 0]")
angle_label.pack()

# === Button ===
def go_home():
    home_angles = [0] * arm.num_joints
    animate_to_angles(home_angles)

home_btn = ttk.Button(frame, text="Reset (Home)", command=go_home)
home_btn.pack(pady=5)

# === Helper functions ===
def draw_arm():
    ax.clear()
    pos = arm.get_positions()
    xs, ys = zip(*pos)
    ax.plot(xs, ys, '-o', color='blue')
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    ax.set_title("Click to Move Arm")
    ax.grid(True)
    if target:
        ax.plot(*target, 'rx', markersize=12, markeredgewidth=2)
    angle_label.config(text=f"Angles: {[round(a, 1) for a in current_angles]}")
    canvas.draw()

def update_current_angles(new_angles):
    global current_angles
    current_angles = new_angles.copy()

def animate_to_angles(target_angles, steps=10, delay=10):
    global current_angles
    diffs = [(t - c) / steps for c, t in zip(current_angles, target_angles)]
    angle_state = current_angles.copy()  # Mutable state for animation

    def step(i=0):
        nonlocal angle_state
        if i >= steps:
            angle_state = target_angles
            arm.set_angles(angle_state)
            update_current_angles(angle_state)
            draw_arm()
            return
        angle_state = [c + d for c, d in zip(angle_state, diffs)]
        arm.set_angles(angle_state)
        update_current_angles(angle_state)
        draw_arm()
        root.after(delay, lambda: step(i + 1))
        send_angles_to_esp32(angle_state)

    step()

def is_target_reachable(x, y):
    arm = RoboticArm(num_joints=3)
    total_length = sum(arm.lengths)
    return np.hypot(x, y) <= total_length

def inverse_kinematics(target_x, target_y):
    def loss_fn(angles):
        arm.set_angles(angles)
        end_x, end_y = arm.get_positions()[-1]
    
        # 1. Target loss
        loss = (end_x - target_x) ** 2 + (end_y - target_y) ** 2

        # 2. Smooth transition penalty
        smooth_penalty = sum([(a - c)**2 for a, c in zip(angles, current_angles)])
    
        # 3. Posture penalty: discourage extreme joint angles (near 0° or 180°)
        posture_penalty = sum([
        1.0 / (abs(a - 90) + 1)  # reward being near 90°, penalize near 0° or 180°
        for a in angles
        ])

        return loss + 0.05 * smooth_penalty + 0.5 * posture_penalty  # Adjust weights
    
     
    initial = arm.angles
    bounds = [(0, 180)] * arm.num_joints
    result = minimize(loss_fn, initial, bounds=bounds)
    if result.success:
        print("IK solved:", result.x)
        animate_to_angles(result.x)
    else:
        print("IK failed.")
    draw_arm()

def on_click(event):
    global target
    if event.xdata is None or event.ydata is None:
        return
    target = (event.xdata, event.ydata)
    inverse_kinematics(*target)
    if not is_target_reachable(event.xdata, event.ydata):
        print("Target is out of reach!")
    return



def send_angles_to_esp32(angles):
    angle_str = ",".join([str(int(a)) for a in angles]) + "\n"
    try:
        esp32.write(angle_str.encode())
    except Exception as e:
        print("Error sending to ESP32:", e)


# === Connect click event ===
canvas.mpl_connect("button_press_event", on_click)

# === Initial Draw ===
draw_arm()
root.mainloop()
