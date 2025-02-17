# Yolo Brawlers

Yolo Brawlers is an OpenCV project created for HackED 2025! You can find more information about this project
on [DevPost](https://devpost.com/software/yolo-brawlers) regarding the project development process, objectives, and motivation.

## Description

Yolo Brawlers is an interactive real-time motion-controlled game where two players control robotic fighters using their own body movements. Using [YOLO V11 Pose Detection](https://github.com/ultralytics/ultralytics), the system translates human fighting moves into commands for the robots, making them punch, weave, and guard dynamically.

## How It Works

1. Pose Detection (YOLO + OpenCV): The system uses YOLO pose estimation to track players' movements in real time.
2. Move Classification: The AI recognizes different fighting poses (punches, weaves, guard stance).
3. Robot Control: Commands are sent to the robots via ESP32-based servo controllers, allowing them to mimic the player's movements.
4. Multiplayer Battle: Two players compete by controlling their own robotic fighters with body movements.

## Tech/Hardware Stack

-   Python, PyQt5 → Graphical user interface (UI) for starting/stopping the game.
-   YOLO (Ultralytics) → Pose detection for movement tracking.
-   OpenCV → Real-time camera feed processing.
-   C++, ESP32, Servo Motors → Robot motion control.

## Getting Started

1. Install conda on your local machine through this [link](https://docs.anaconda.com/anaconda/install/) or through the OS package manager provided.
2. For Apple Silicon based chips:
    - Create your conda environment using `conda create -n ultralytics-env python=3.12 -y`.
3. For AMD/Intel based chips:
    - Create your conda enviroment using `CONDA_SUBDIR=osx-arm64 conda create -n ultralytics-env python=3.12 -y`.
4. Enter the conda environment by entering `conda activate ultralytics-env`.
5. Install necessary python libraries in conda environment using `pip install -r requirements.txt`.
6. Run the project inside the UI folder using `python3 finalUI.py`.

## Gallery
![19C21752-C7D1-428F-B070-E98F84A3DB98_4_5005_c](https://github.com/user-attachments/assets/cdbb7106-7beb-42ac-8e96-8922efde17bd)

![A03617F5-B129-4E75-8066-61DCA39BA716_1_105_c](https://github.com/user-attachments/assets/48f259d2-46df-4306-810c-89036a56abc7)

## Notes

-   For Macbook Intel Chip you need to install `pip install "numpy<2"` manually.
-   For any Apple Silicon Chips you cannot access the keyboard controller.

## Resources

-   [Ultralytics Coco Pose Estimation](https://docs.ultralytics.com/datasets/pose/coco/)
-   [Ultralytics Pose Estimation Tasks](https://docs.ultralytics.com/tasks/pose/)

## Team Members

1. [Aron Gu](https://github.com/arongu321)
2. [Sami Jagirdar](https://github.com/Sami-Jagirdar)
3. [Jared Drueco](https://github.com/jdrco)
4. [Antonio Martin-Ozimek](https://github.com/antonio2uofa)
