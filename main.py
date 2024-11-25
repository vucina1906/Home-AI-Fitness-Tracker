import tkinter as tk
from threading import Thread
from exercises.biceps_curl import run_biceps_curl
from exercises.shoulder_press import run_shoulder_press
from exercises.shoulder_lateral import run_shoulder_lateral
from exercises.shoulder_front import run_shoulder_front
from exercises.overhead_extension import run_overhead_extension
from exercises.squat import run_squat
from exercises.knees_up import run_knees_up
from exercises.side_bend import run_side_bend
import ttkbootstrap as ttk  # Importing ttkbootstrap for rounded buttons

# Function to start exercises in separate threads
def start_shoulder_press(): Thread(target=run_shoulder_press).start()
def start_biceps_curl(): Thread(target=run_biceps_curl).start()
def start_shoulder_lateral(): Thread(target=run_shoulder_lateral).start()
def start_shoulder_front(): Thread(target=run_shoulder_front).start()
def start_overhead_extension(): Thread(target=run_overhead_extension).start()
def start_squat(): Thread(target=run_squat).start()
def start_knees_up(): Thread(target=run_knees_up).start()
def start_side_bend(): Thread(target=run_side_bend).start()

# Mapping button text, commands, image paths, positions, dimensions, and descriptions
exercises = [
    # Format: (Text, Command, Image Path, Image Position (x, y), Image Size (width, height), Button Position (x, y), Description, Description Position)
    ("Shoulder Press", start_shoulder_press, "static/shoulder_press.png", (55, 150), (130, 100), (50, 270),
     "The shoulder press is a fundamental exercise that strengthens the shoulders, triceps, and upper chest. It enhances overhead stability and builds core strength, making it ideal for improving posture and upper body endurance.", (300, 150)),
    ("Biceps Curl", start_biceps_curl, "static/biceps_curl.png", (27, 360), (170, 90), (50, 470),
     "The biceps curl is a classic arm exercise that targets the biceps muscles. It helps build strength and definition in the arms, improving grip and forearm stability for everyday activities and athletic performance.", (300, 360)),
    ("Shoulder Lateral", start_shoulder_lateral, "static/shoulder_lateral.png", (65, 550), (130, 100), (50, 670),
     "The shoulder lateral raise targets the deltoid muscles, enhancing shoulder width and definition. This exercise improves upper body symmetry and helps in developing strong, rounded shoulders for better posture and strength.", (300, 550)),
    ("Shoulder Front", start_shoulder_front, "static/shoulder_front.png", (60, 750), (130, 90), (50, 870),
     "The shoulder front raise focuses on the anterior deltoid muscles, enhancing shoulder strength and definition. This exercise improves upper body stability and supports better posture and functional movement.", (300, 750)),
    ("Overhead Extension", start_overhead_extension, "static/overhead_extension.png", (1150, 150), (180, 105), (1200, 270),
     "The overhead extension isolates the triceps, building strength and tone in the back of the arms. This exercise enhances upper body stability and is essential for improving arm endurance and functionality.", (900, 150)),
    ("Squat", start_squat, "static/squat.png", (1200, 350), (130, 95), (1200, 470),
     "The squat is a foundational exercise that strengthens the legs, glutes, and core. It improves lower body power, balance, and mobility, making it essential for overall functional strength and athletic performance.", (900, 360)),
    ("Knees Up", start_knees_up, "static/knees_up.png", (1180, 550), (150, 120), (1200, 670),
     "Improve your core and cardiovascular health by raising your knees alternately.It improves balance, coordination, and flexibility while engaging the hip flexors and abdominal muscles for a full-body workout.", (900, 550)),
    ("Side Bend", start_side_bend, "static/side_bend.png", (1200, 730), (150, 130), (1200, 870),
     "Stretch and strengthen your obliques with this dynamic side-to-side movement.This exercise helps sculpt the waistline, enhances spinal mobility, and supports better balance and posture.", (900,750)),
]

# Helper function to resize images
def load_image(path, size):
    try:
        img = tk.PhotoImage(file=path)
        img = img.subsample(max(img.width() // size[0], 1), max(img.height() // size[1], 1))
        return img
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

# Initialize the ttkbootstrap theme
root = ttk.Window(themename="flatly")  # Choose a modern theme
root.title("Home AI Fitness Tracker")
root.geometry("1400x1000")  # Set window size

# Main title
title_label = ttk.Label(
    root,
    text="Home AI Fitness Tracker",
    font=("Arial", 30, "bold"),
    bootstyle="primary"
)
title_label.place(x=500, y=20)  # Centered title

# Add images, buttons, and descriptions with specified positions
for text, command, image_path, img_position, img_size, btn_position, description, desc_position in exercises:
    # Load and display the resized image at its specified position
    img = load_image(image_path, img_size)
    if img:
        img_label = ttk.Label(root, image=img)
        img_label.image = img  # Keep a reference to prevent garbage collection
        img_label.place(x=img_position[0], y=img_position[1])

    # Create rounded button
    btn = ttk.Button(
        root,
        text=text,
        command=command,
        bootstyle="success-outline",  # Rounded, modern style
        width=20,
    )
    btn.place(x=btn_position[0], y=btn_position[1])

    # Add description bubble
    desc_label = ttk.Label(
        root,
        text=description,
        #font=("Helvetica", 12, "italic"),
        font=("Comic Sans MS", 12, "bold"),
        bootstyle="info",  # Bubble-like style
        wraplength=300,  # Set text wrapping width
        anchor="center"
    )
    desc_label.place(x=desc_position[0], y=desc_position[1])

# Run the GUI
root.mainloop()
