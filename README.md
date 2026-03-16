# lego-autonomous-edge
Teleop and Autonomy Educational Project with Lego, using Lego Technic™ #42160 - Audi RS Q e-tron

# Autonomous Edge Stack for Pybricks

A browser-based, zero-backend telemetry and autonomous driving stack for Lego Technic vehicles. This project transforms an Android phone into an edge-compute relay and uses WebRTC to provide infinite-range global control, sensor fusion, and AI-powered Autonomous Emergency Braking (AEB).

## System Architecture

The stack is divided into three components:
1. **The Physical Layer (`hub.py`):** Runs on the Pybricks Smart Hub. Handles direct motor control and parses Bluetooth Low Energy (BLE) commands.
2. **The Edge Relay (`phone.html`):** Runs on an Android phone strapped to the vehicle. It captures the camera feed, executes Sensor Fusion (GPS + 3D IMU Magnetometer) for stable heading calculation, and acts as the WebRTC signaling bridge.
3. **The Command Cockpit (`controller.html`):** Runs on the operator's mobile device anywhere in the world. It processes the live video feed through an edge-AI model to detect collision threats and provides a map-based UI for plotting autonomous GPS waypoints.

## Key Features
* **Global WebRTC Telemetry:** Sub-150ms video and command latency over 4G/5G/Wi-Fi using PeerJS.
* **AI Autonomous Emergency Braking (AEB):** Utilizes TensorFlow.js (`coco-ssd`) to detect humans, pets, and vehicles. If an object crosses the dynamic trajectory corridor, the system automatically fires an emergency brake command via BLE.
* **Sensor Fusion Navigation:** Combines raw GPS coordinates with Low-Pass filtered IMU Magnetometer data to provide rock-solid headings, eliminating GPS jitter at low speeds.
* **Autonomous Waypoint Routing:** Allows operators to plot up to 20 GPS waypoints on a Leaflet map and executes a non-blocking navigation loop to drive the car autonomously to the target.

## Setup & Deployment
No backend server or Python hosting is required. 
1. Flash `hub.py` to your Pybricks compatible Lego Hub, using - https://code.pybricks.com/
2. Run local server on Andoird Phone. I useed Termux app. https://play.google.com/store/apps/details?id=com.termux&hl=en_US
Once installed, Run the local server - `python -m http.server 8000.`
Then open 'phone.html' a local HTTP server and access it on the car's Android phone via `http://localhost:8000/phone.html` (Localhost is required to bypass Chrome's Web Bluetooth security restrictions). 
4. Connect the phone to the Lego Hub via the UI.
5. Open `controller.html` on your remote device, enter the 4-digit generated PIN, and initiate the satellite link.

## System Diagram :
[ Controller Phone ] <======= WebRTC (PeerJS) =======> [ Edge Phone (Mounted) ]
 (Teleop UI, Map)          (Global Cellular/Wi-Fi)      (Camera, GPS, 3D IMU)
        |                                                        |
  [ TFJS AI ]                                               [ Web BLE ]
(AEB Override)                                                   |
                                                                 V
                                                          [ Pybricks Hub ]
                                                       (Steering & Drive Motors)

Install  <img width="200" height="500" alt="Screenshot TO" src="https://github.com/user-attachments/assets/06133cca-1da6-45d6-ad2d-eecb77fdefb9" />
TO UX  <img width="200" height="500" alt="Screenshot TO" src="https://github.com/user-attachments/assets/7027f5be-09ca-48ac-b63e-418ec27e7aff" />
Auto UX  <img width="200" height="500" alt="Screenshot-Auto mode" src="https://github.com/user-attachments/assets/b57b336d-491c-46a8-ba40-b7a4064f2351" />

                  

## Open Source Acknowledgments
This project was built using the following open-source :
-Pybricks: Python coding for smart LEGO® hubs. (MIT License)
-TensorFlow.js: Machine learning in JavaScript. (Apache License 2.0)
-PeerJS: Simple peer-to-peer with WebRTC. (MIT License)
-Leaflet.js: Interactive mobile-friendly maps. (BSD-2-Clause License)
-Map Data & Tiles: Map tiles by Carto (CC BY 3.0), under atmospheric data by OpenStreetMap (ODbL).

## License
This project is licensed under the MIT License - see the LICENSE file for details.
